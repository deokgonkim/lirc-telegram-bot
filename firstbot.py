from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def tvPower(bot, update):
    import subprocess
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))
    result = subprocess.check_output(['irsend', 'SEND_ONCE', 'Samsung', 'KEY_POWER'])
    update.message.reply_text('I turned on TV... error(%s)' % result)


def help(bot, update):
    logging.info('I got command %s - %s' % (update.update_id, update.message.text))
    update.message.reply_text('''Here is help!
/help   : This message
/tvpower: Turn on/off television.
''')


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

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("tvpower", tvPower))
    dp.add_handler(CommandHandler("help", help))

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
    token = raw_input('Enter bot token: ')
    main(token)
