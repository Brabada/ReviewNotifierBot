import logging
import pprint
from time import sleep

import requests
from environs import Env
import telegram


def send_message_by_bot(bot_credentials, checked_lessons):
    bot = telegram.Bot(token=bot_credentials['bot_token'])
    chat_id = bot_credentials['chat_id']
    intro_message = f'У вас проверили работу "{checked_lessons["lesson_title"]}."'
    lesson_url_message = f'Ссылка на работу: {checked_lessons["lesson_url"]}'
    if checked_lessons['is_negative']:
        result_message = 'К сожалению в работе нашлись ошибки.'
    else:
        result_message = 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
    message = f'{intro_message}\n\n{lesson_url_message}\n\n{result_message}'
    bot.send_message(chat_id=chat_id, text=message)


def main():

    env = Env()
    env.read_env()
    if env.bool("LOGGING_DEBUG"):
        logging.basicConfig(level=logging.DEBUG)

    telegram_user_token = env.str("TELEGRAM_USER_TOKEN")
    timestamp = None
    bot_credentials = {
        'bot_token': env.str("TELEGRAM_BOT_TOKEN"),
        'chat_id': env.int('TELEGRAM_CHAT_ID'),
    }

    while True:
        try:
            headers = {
                'Authorization': f'Token {telegram_user_token}',
            }

            url = 'https://dvmn.org/api/long_polling/'
            timeout = 100

            logging.debug(f'1. Timestamp is {timestamp}')
            payload = {'timestamp': timestamp}
            response = requests.get(url=url, headers=headers, timeout=timeout, params=payload)

            response.raise_for_status()
            checked_lessons = response.json()

            if checked_lessons["status"] == "timeout":
                timestamp = checked_lessons["timestamp_to_request"]
            else:
                send_message_by_bot(bot_credentials, checked_lessons['new_attempts'][0])
        except requests.HTTPError:
            logging.error("Can't retrieve review list from API.")
        except requests.exceptions.ReadTimeout:
            logging.warning('Timeout reached out.')
        except requests.exceptions.ConnectionError:
            logging.warning('Connection is broken.')
            sleep(100)


if __name__ == "__main__":
    main()
