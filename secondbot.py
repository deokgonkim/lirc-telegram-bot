#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime 
import functools
import pika
import threading

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class DHT11(object):

    current_temperature = None
    current_humidity = None

def start_consuming():
    def receive_temperature(ch, method, properties, body):
        print('received temperature - {}'.format(body))
        DHT11.current_temperature = '{} - {}*C'.format(datetime.datetime.now(), body)

    def receive_humidity(ch, method, properties, body):
        print('received humidity - {}'.format(body))
        DHT11.current_humidity = '{} - {}%'.format(datetime.datetime.now(), body)

    connection = pika.BlockingConnection(pika.ConnectionParameters('server'))
    channel = connection.channel()
    
    channel.basic_consume(queue='temperature',
                          auto_ack=True,
                          on_message_callback=receive_temperature)
    
    channel.basic_consume(queue='humidity',
                          auto_ack=True,
                          on_message_callback=receive_humidity)
    
    channel.start_consuming()

t = threading.Thread(target=start_consuming)
t.setDaemon(True)
t.start()
    
def irsend(device, key):
    import subprocess
    result = ''
    try:
        result = subprocess.check_output(['irsend', 'SEND_ONCE', device, key])
    except Exception, e:
        result = str(e)
    return result.strip()


COMMANDS = []


def IrCommand(fn):
    d = dict()
    d['name'] = fn.__name__
    d['desc'] = fn.__doc__

    @functools.wraps(fn)
    def wrapped_fn(*args, **kwargs):
        return fn(*args, **kwargs)

    d['fn'] = wrapped_fn
    COMMANDS.append(d)

    return wrapped_fn


class LG_AC(object):
    device = 'lgac.conf'

    @IrCommand
    def ac_on(self, bot, update):
        """AC Power On"""
        return self.cmd('power-on', bot, update)

    @IrCommand
    def ac_off(self, bot, update):
        """AC Power Off"""
        return self.cmd('power-off', bot, update)

    @IrCommand
    def ac_temp18(self, bot, update):
        """AC Temperature 18"""
        return self.cmd('temperature-18', bot, update)

    @IrCommand
    def ac_temp26(self, bot, update):
        """AC Temperature 26"""
        return self.cmd('temperature-26', bot, update)

    @IrCommand
    def ac_jeton(self, bot, update):
        """AC Jet On"""
        return self.cmd('jet-on', bot, update)

    @IrCommand
    def ac_jetoff(self, bot, update):
        """AC Jet Off"""
        return self.cmd('jet-off', bot, update)

    def cmd(self, key, bot, update):
        logging.info('I got command {update_id} - {message.text}'.format(
                     update_id=update.update_id,
                     message=update.message))
        result = irsend(self.device, key)
        if len(result) == 0:
            msg = 'I pressed {key} button on {device}...'
            update.message.reply_text(msg.format(key=key, device=self.device))
        else:
            msg = 'I pressed {key} button on {device}... - error {result}'
            update.message.reply_text(msg.format(key=key, device=self.device, result=result))
        update.message.reply_text('''Additional commands.
{}
/help : For more help.
'''.format('\n'.join([ '{} : {}'.format('/' + item['name'], item['desc']) for item in COMMANDS])))
        return result


def tvPower(bot, update):
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))
    result = irsend('Samsung', 'KEY_POWER')
    if len(result) == 0:
        update.message.reply_text('I pressed POWER button on TV...')
    else:
        update.message.reply_text('I pressed POWER button on TV... got error - %s' % result)


def show_temperature(bot, update):
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))
    update.message.reply_text(DHT11.current_temperature)

def show_humidity(bot, update):
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))
    update.message.reply_text(DHT11.current_humidity)


def help(bot, update):
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))

    help_msg = '''Here is help!
/help : This message
/tvpower : Turn on/off television.
/temperature : Show current Temperature
/humidity : Show current Humidity
'''
    help_msg += '\n'.join([ '/{} : {}'.format(item['name'], item['desc']) for item in COMMANDS])

    update.message.reply_text(help_msg)


def echo(bot, update):
    logging.info('I got message %s - %s' % (update.update_id, update.message.text))
    update.message.reply_text('I can repeat your message. If you want to command me. check /help')
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main(token):
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    ac = LG_AC()

    dp.add_handler(CommandHandler("help", help))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("tvpower", tvPower))

    dp.add_handler(CommandHandler("temperature", show_temperature))
    dp.add_handler(CommandHandler("humidity", show_humidity))

    for item in COMMANDS:
        #def fn(*args, **kwargs):
        #    getattr(ac, item['name']).__call__(ac, *args, **kwargs)
        #dp.add_handler(CommandHandler(item['name'], fn))
        #dp.add_handler(CommandHandler(item['name'], item['fn']))
        dp.add_handler(CommandHandler(item['name'], getattr(ac, item['name'])))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    import os
    #token = raw_input('Enter bot token: ')
    tokenfile = os.path.join(os.environ['HOME'], '.bot_token')
    token = open(tokenfile, 'r').read().strip()
    print('token - {}'.format(token))
    main(token)
