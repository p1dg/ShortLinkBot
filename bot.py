# Initial module to run bot

import logging
import sqlite3

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters

import commands
import messages
from settings import config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='Bot.log')

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    logger.info("Initializing database")
    conn = sqlite3.connect(config['DATABASE'])
    cursor = conn.cursor()

    try:
        request = """
        CREATE TABLE bot_history
        (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INT, link VARCHAR, short_link VARCHAR)
        """
        cursor.execute(request)
    except sqlite3.OperationalError as e:
        logger.info(e)

    logger.info("Initializing bot")
    updater = Updater(token=config['TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', commands.start), 1)
    dispatcher.add_handler(CommandHandler('help', 	commands.help), 1)
    dispatcher.add_handler(CommandHandler('history',  commands.history), 1)

    dispatcher.add_handler(MessageHandler(Filters.text & ~
                                  Filters.command, messages.chat))

    dispatcher.add_error_handler(error)

    print("\nrunning...\n")
    logger.info("The bot is enabled")

    updater.start_polling()
    updater.idle()
    
    logger.info("The bot is disabled")


if __name__ == '__main__':
    main()
