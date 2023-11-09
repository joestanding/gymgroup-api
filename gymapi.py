import requests
import json
import logging
import sys
from requests.compat import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GymGroupAPI:

    BASE_URL = 'https://thegymgroup.netpulse.com/np/'
    ENDPOINT_LOGIN = 'exerciser/login'
    STATE_FILE = 'state.json'
    REQ_HEADERS = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/3.12.3',
        'X-NP-API-Version': '1.5',
        'X-NP-App-Version': '5.0',
        "X-NP-User-Agent": "clientType=MOBILE_DEVICE; " \
                "devicePlatform=ANDROID; " \
                "deviceUid=; " \
                "applicationName=The Gym Group; " \
                "applicationVersion=5.0; " \
                "applicationVersionCode=38"
    }


    def __init__(self, username, password):
        self.username   = username
        self.password   = password
        self.user_id    = None
        self.home_gym   = None
        self.api_sess   = requests.session()
        self.api_sess.headers = self.REQ_HEADERS

        if not self._load_state():
            logger.debug("State file didn't exist or failed to load, logging..")
            if not self.login():
                logger.error("Authentication failed! Check credentials.")

    
    def _api_req(self, method, endpoint, data=None, retry_on_auth_fail=True):
        if method != 'POST' and method !='GET':
            logger.error("Invalid HTTP method specified to _api_req!")
            return False

        final_url = urljoin(self.BASE_URL, endpoint)
        logger.debug(f"API {method} to URL '{final_url}'..")

        try:
            if method.upper() == 'POST':
                response = self.api_sess.post(final_url, data=data)
                response.raise_for_status()
            elif method.upper() == 'GET':
                response = self.api_sess.get(final_url)
                response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            logger.error(f"HTTP error {response.status_code} on API {method}! " \
                    f"Error: {exc}")
            if response.status_code == 403 and retry_on_auth_fail:
                logger.error("Server returned auth. failure, logging in..")
                if not self.login():
                    logger.error("Authentication retry failed!")
                    return False
                return self._api_req(method, endpoint, data, False)
            return False
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Connection error on API {method}! Error: {exc}")
            return False
        except requests.exceptions.Timeout as exc:
            logger.error(f"Timeout error on API {method}! Error: {exc}")
            return False
        except requests.exceptions.RequestException as exc:
            logger.error(f"Misc. error on API {method}! Error: {exc}")
            return False

        logger.debug(f"API {method} to '{endpoint}' succeeded!")
        logger.debug(f"Response: {response}")

        return response

    
    def _load_state(self):
        try:
            with open(self.STATE_FILE, 'r') as file_handle:
                state = json.load(file_handle)
                self.api_sess.cookies.update(state['cookies'])
                self.user_id  = state['login_resp']['uuid']
                self.home_gym = state['login_resp']['homeClubUuid']
                return True
        except Exception as exc:
            logger.error(f"Exception occurred loading cookie jar: {exc}")
            return False


    def _save_state(self, state):
        with open(self.STATE_FILE, 'w') as file_handle:
            json.dump(state, file_handle)


    def login(self):
        if not self.username or not self.password:
            logger.error("Username or password were not specified!")
            return False

        logger.debug(f"Authenticating with username '{self.username}'")
        response = self._api_req('POST', self.ENDPOINT_LOGIN, {
            'username': self.username,
            'password': self.password
        })

        if not response:
            logger.error("There was a failure to log in!")
            return False

        try:
            resp_json = response.json()
        except json.JSONDecodeError as exc:
            logger.error(f"Login response was not valid JSON! Exc: {exc}")
            return False

        self.user_id  = resp_json['uuid']
        self.home_gym = resp_json['homeClubUuid']

        logger.debug(f"Authenticated as UUID: {self.user_id}")
        logger.debug(f"Storing cookies to disk..")
        cookies = requests.utils.dict_from_cookiejar(self.api_sess.cookies)

        state = { 'cookies': cookies, 'login_resp': resp_json }
        self._save_state(state)
        
        return True
    

    def get_gym_occupancy(self, gym_uuid):
        endpoint = f"thegymgroup/v1.0/exerciser/{self.user_id}/gym-busyness?" \
                f"gymLocationId={gym_uuid}"
        response = self._api_req('GET', endpoint)

        if not response:
            logger.error("Failed to retrieve gym occupancy!")
            return False

        try:
            resp_json = response.json()
        except json.JSONDecodeError as exc:
            logger.error(f"Gym occupancy response was not valid JSON! Exc: {exc}")
            return False
        
        logger.debug(f"Gym occupancy JSON: {json}")
        return resp_json.get('currentCapacity')
