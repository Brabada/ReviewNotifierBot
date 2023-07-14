import logging
import pprint
from time import sleep

import requests
from environs import Env


def long_poll_review_list(personal_token, timestamp=0):

    headers = {
        'Authorization': f'Token {personal_token}',
    }

    url = 'https://dvmn.org/api/long_polling/'
    timeout = 100
    try:
        if timestamp:
            logging.debug(f'1. Timestamp is {timestamp}')
            payload = {'timestamp': timestamp}
            response = requests.get(url=url, headers=headers, timeout=timeout, params=payload)
        else:
            logging.debug(f'2. Timestamp is {timestamp}')
            response = requests.get(url=url, headers=headers, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        logging.warning('Timeout reached out.')
        return
    except requests.exceptions.ConnectionError:
        logging.warning('Connection is broken.')
        sleep(timeout)
        return

    response.raise_for_status()
    response_json = response.json()
    pprint.pprint(response_json)

    if response_json["status"] == "timeout":
        return response_json["timestamp_to_request"]


def main():

    logging.basicConfig(level=logging.DEBUG)
    env = Env()
    env.read_env()
    token = env.str("PERSONAL_TOKEN")
    timestamp = 0
    try:
        while True:
            timestamp = long_poll_review_list(token, timestamp)
    except requests.HTTPError:
        logging.error("Can't retrieve review list from API.")


if __name__ == "__main__":
    main()
