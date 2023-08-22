import logging
import pprint
from time import sleep

import requests
from environs import Env
import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot_token, chat_id):
        super().__init__()
        self.tg_bot = telegram.Bot(token=tg_bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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

    telegram_user_token = env.str("TELEGRAM_USER_TOKEN")
    timestamp = None
    bot_credentials = {
        'bot_token': env.str("TELEGRAM_BOT_TOKEN"),
        'chat_id': env.int('TELEGRAM_CHAT_ID'),
    }
    logging.basicConfig(format='%(message)s')
    logger = logging.getLogger('telegram_bot')
    if env.bool("LOGGING_DEBUG"):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.addHandler(TelegramLogsHandler(tg_bot_token=bot_credentials['bot_token'], chat_id=bot_credentials['chat_id']))

    logger.info('Бот начал работу')

    while True:
        try:
            headers = {
                'Authorization': f'Token {telegram_user_token}',
            }

            url = 'https://dvmn.org/api/long_polling/'
            timeout = 100

            logger.debug(f'1. Timestamp is {timestamp}')
            payload = {'timestamp': timestamp}
            response = requests.get(url=url, headers=headers, timeout=timeout, params=payload)

            response.raise_for_status()
            checked_lessons = response.json()

            if checked_lessons["status"] == "timeout":
                timestamp = checked_lessons["timestamp_to_request"]
            else:
                timestamp = checked_lessons['last_attempt_timestamp']
                send_message_by_bot(bot_credentials, checked_lessons['new_attempts'][0])
        except requests.HTTPError:
            logger.error("Can't retrieve review list from API.")
        except requests.exceptions.ReadTimeout:
            logger.warning('Timeout reached out.')
        except requests.exceptions.ConnectionError:
            logger.warning('Connection is broken.')
            sleep(100)
    logger.info('bot is shutdown')


if __name__ == "__main__":
    main()
