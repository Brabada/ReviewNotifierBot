import logging
import pprint
from time import sleep

import requests
from environs import Env
import telegram


def send_message_by_bot(bot_credentials, response):
    bot = telegram.Bot(token=bot_credentials['bot_token'])
    chat_id = bot_credentials['chat_id']
    intro_message = f'У вас проверили работу "{response["lesson_title"]}."'
    lesson_url_message = f'Ссылка на работу: {response["lesson_url"]}'
    if response['is_negative']:
        result_message = 'К сожалению в работе нашлись ошибки.'
    else:
        result_message = 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
    message = f'{intro_message}\n\n{lesson_url_message}\n\n{result_message}'
    bot.send_message(chat_id=chat_id, text=message)


def long_poll_review_list(personal_token, bot_credentials, timestamp=0):

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
    response = response.json()

    if response["status"] == "timeout":
        return response["timestamp_to_request"]
    else:
        send_message_by_bot(bot_credentials, response['new_attempts'][0])


def main():

    env = Env()
    env.read_env()
    if env.bool("LOGGING_DEBUG"):
        logging.basicConfig(level=logging.DEBUG)

    personal_token = env.str("PERSONAL_TOKEN")
    timestamp = 0
    bot_credentials = {
        'bot_token': env.str("BOT_TOKEN"),
        'chat_id': env.int('chat_id'),
    }

    try:
        while True:
            timestamp = long_poll_review_list(personal_token, bot_credentials, timestamp)
    except requests.HTTPError:
        logging.error("Can't retrieve review list from API.")


if __name__ == "__main__":
    main()
