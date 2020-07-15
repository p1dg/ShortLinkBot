# bot's messages' comandad

import logging
import requests
import sqlite3
import time

from telegram.ext.dispatcher import run_async

from settings import config

logger = logging.getLogger(__name__)


def get_short_url(url):
    try:
        response = requests.post(
            "https://rel.ink/api/links/", data={"url": url}).json()

        if response["url"] == url:
            return "https://rel.ink/{}".format(response["hashid"])
        else:
            return "Invalid URL"
    except Exception as e:
        time.sleep(1)
        return get_short_url(url)

@run_async
def chat(bot, update):
    logger.info(f"User {update.message.chat_id} sendmessage {update.message.text}")
    link = get_short_url(update.message.text)

    if link == "Invalid URL":
        bot.send_message(chat_id=update.message.chat_id, text=link)
        logger.info(f"User {update.message.chat_id} shorted link incorrect")
        return

    conn = sqlite3.connect(config['DATABASE'])
    cursor = conn.cursor()

    request = """
        INSERT INTO bot_history(chat_id, link, short_link)
        VALUES ({}, '{}', '{}')
    """.format(update.message.chat_id, link, update.message.text)

    cursor.execute(request)
    conn.commit()

    bot.send_message(chat_id=update.message.chat_id, text=link)

    logger.info(f"User {update.message.chat_id} shorted link correct")
