from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import logging
import re
import configparser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

updater=Updater(token=config['BOT']['TOKEN'])
dispatcher=updater.dispatcher

def getID(bot, update):
    print("Channel ID = " + str(update.channel_post.chat.id))

dispatcher.add_handler(MessageHandler(Filters.text, getID))

updater.start_polling()
