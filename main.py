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
timestamp = [datetime.datetime.now().timestamp()]
while True:
    try:
        response = requests.get(f'https://dvmn.org/api/long_polling/?timestamp={int(timestamp[0])}',
                                headers={'Authorization': f'Token {DEVMAN_TOKEN}'},
                                timeout=100)
        response.raise_for_status()
        for solution in response.json().get('new_attempts', []):
            date = datetime.datetime.fromtimestamp(solution['timestamp'])
            status = '\u2757\ufe0f Надо потрудиться :(' if solution['is_negative'] else '\u2705 Работа принята'
            text = f"<i>Дата: {date.strftime('%d-%m-%Y %H:%M')}</i>\n" \
                   f"<b>{status}</b>\n" \
                   f"{solution['lesson_title']}\n" \
                   f"https://dvmn.org{solution['lesson_url']}"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode='HTML')
        timestamp[0] = (response.json().get('timestamp_to_request') or response.json().get(
            'last_attempt_timestamp')) + 1
    except requests.exceptions.ReadTimeout:
        timestamp[0] = datetime.datetime.now().timestamp() - 1
    except requests.exceptions.ConnectionError:
        print('Error connection')
        time.sleep(10)
