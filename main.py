import datetime
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')

bot = telegram.Bot(token=TELEGRAM_TOKEN)
timestamp = datetime.datetime.now().timestamp()
template_message = '''<i>Дата: {}</i>
<b>{}</b>
{}
https://dvmn.org{}
'''
while True:
    try:
        response = requests.get(f'https://dvmn.org/api/long_polling/',
                                params={'timestamp': timestamp},
                                headers={
                                    'Authorization': f'Token {DEVMAN_TOKEN}'},
                                timeout=10)
        response.raise_for_status()
        response_body = response.json()
        for solution in response_body.get('new_attempts', []):
            date = datetime.datetime.fromtimestamp(solution['timestamp'])
            status = ('\u2757\ufe0f Надо потрудиться :('
                      if solution['is_negative']
                      else '\u2705 Работа принята')

            message = template_message.format(
                date.strftime('%d-%m-%Y %H:%M'),
                status,
                solution['lesson_title'],
                solution['lesson_url']
            )

            bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                             text=message,
                             parse_mode='HTML')

        timestamp = response_body.get(
            'timestamp_to_request') or response_body.get(
            'last_attempt_timestamp')
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectionError:
        print('Connection error')
        time.sleep(10)
