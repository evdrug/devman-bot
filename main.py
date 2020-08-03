import datetime
import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


class TelegramLogsHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = telegram.Bot(token=self.telegram_token)

    def emit(self, record):

        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.telegram_chat_id,
                              text=log_entry,
                              )


DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
TEMPLATE_MESSAGE = '''\ud83d\udd52 {}
{}
{}
https://dvmn.org{}
'''

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler())

    timestamp = datetime.datetime.now().timestamp()
    interval = 1
    logger.info('\u2705 Бот запущен')
    while True:
        try:
            print(0/0)
            response = requests.get(f'https://dvmn.org/api/long_polling/',
                                    params={'timestamp': timestamp},
                                    headers={
                                        'Authorization': f'Token {DEVMAN_TOKEN}'},
                                    timeout=60)
            response.raise_for_status()
            response_body = response.json()
            for solution in response_body.get('new_attempts', []):
                date = datetime.datetime.fromtimestamp(solution['timestamp'])
                status = ('\u2757\ufe0f Надо потрудиться \ud83d\ude14'
                          if solution['is_negative']
                          else '\u2705 Работа принята \ud83c\udf89')

                message = TEMPLATE_MESSAGE.format(
                    date.strftime('%d-%m-%Y %H:%M'),
                    status,
                    solution['lesson_title'],
                    solution['lesson_url']
                )

                logger.info(message)

            timestamp = response_body.get(
                'timestamp_to_request') or response_body.get(
                'last_attempt_timestamp')
            interval = 1
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError as e:
            logger.warning(f'\ud83c\udd98 Connection error <br> {e}')
            time.sleep(10)
        except Exception as e:
            logger.exception(e)
            time.sleep(10*interval)
            interval += 1
