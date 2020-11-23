from flask import Flask, request, jsonify
from flask_sslify import SSLify
from util import get_quote, parse_text

import requests


# Import configuration parameters
try:
    import configuration as conf
except ModuleNotFoundError:
    raise ModuleNotFoundError("""Configuration file is not present.
        Please define 'configuration.py' per the documentation.""")

# Make sure required configuration parameters is set
for parameter in ['TOKEN', 'API_KEY']:
    if not hasattr(conf, parameter):
        raise RuntimeError(
            f'Required parameter {parameter} is missing from configuration.py.'
        )


TELEGRAM_URL = f'https://api.telegram.org/bot{conf.TOKEN}/'
BASE_URL = f'/{conf.TOKEN}/'
API_KEY = conf.API_KEY


# Configure application
app = Flask(__name__)
sslify = SSLify(app)


def send_message(chat_id, text):
    """Send text messages back to chat."""

    url = f'{TELEGRAM_URL}sendMessage'
    message = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}

    response = requests.post(url, json=message)

    return response.json()


def format_message(obj):
    """Format message with Markdown V2."""

    md = '<strong>{}</strong>\nprice: {}\nupdate: {}'.format(
        obj.get('name', ''),
        obj.get('price', ''),
        obj.get('upd_time', ''),
    )

    return md
# https://api.telegram.org/bot1442875355:AAEmoc1YyMppJxDNuJf9RlqXAG0RcFJ7ZzY/setWebhook?url=https://13581086b42c.ngrok.io/1442875355:AAEmoc1YyMppJxDNuJf9RlqXAG0RcFJ7ZzY/


@app.route(BASE_URL, methods=['POST'])
def index():
    if request.method == 'POST':
        response = request.get_json()

        chat_id = response['message']['chat']['id']
        text = response['message']['text']

        symbol = parse_text(text)
        # Commands not found
        if symbol is None:
            return jsonify(response)

        obj = get_quote(symbol, API_KEY)
        if obj is not None:
            send_message(chat_id, format_message(obj))
        else:
            send_message(chat_id, f'Command "{symbol}" is missing.')

        return jsonify(response)


if __name__ == '__main__':
    app.run()
