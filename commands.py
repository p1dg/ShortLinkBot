# bot's coomands

import logging
import sqlite3

from telegram.ext.dispatcher import run_async

from settings import config
import text_for_Bot

logger = logging.getLogger(__name__)


@run_async
def start(bot, update):
    logger.info(f"Chat {update.message.chat_id} used command /start")
    bot.send_message(chat_id=update.message.chat_id,
                     text=text_for_Bot.start_text)

@run_async
def help(bot, update):
    logger.info(f"Chat {update.message.chat_id} used command /help")
    bot.send_message(chat_id=update.message.chat_id,
                     text=text_for_Bot.help_text)

@run_async
def history(bot, update):
    logger.info(f"User {update.message.chat_id} used command /history")

    conn = sqlite3.connect(config['DATABASE'])
    cursor = conn.cursor()

    request = """
    SELECT * FROM bot_history
    WHERE chat_id = {}
    ORDER BY id DESC
    LIMIT 10
	""".format(update.message.chat_id)

    cursor.execute(request)
    links = cursor.fetchall()

    if len(links) == 0:
        bot.send_message(chat_id=update.message.chat_id, text="Empty history(")
        return

    for row in links:
        text = "old: {}\nshortened: {}\n".format(row[3], row[2])
        bot.send_message(chat_id=update.message.chat_id, text=text)
