import logging

import telegram

import time

from telegram.error import NetworkError, Unauthorized

logging.basicConfig(level=logging.INFO)

def main(token):
    bot = telegram.Bot(token=token)

    try:
        update = bot.get_updates()[0]
        update_id = update.update_id
        logging.info('First got message %s - %s' % (update_id, update.message.text))
    except IndexError:
        update_id = None

    while True:
        try:
            echo(bot, update_id)
            time.sleep(1)
        except NetworkError:
            logging.error('Network Error', exc_info=True)
        except Unauthorized:
            logging.error('Unauthorized Error occured', exc_info=True)
            update_id += 1

def echo(bot, update_id):
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:
            text = update.message.text
            logging.info('Got message %s - %s' % (update.update_id, update.message.text))
            update.message.reply_text('Re: %s' % text)

if __name__ == '__main__':
    token = raw_input('Enter bot token: ')
    main(token)
