from telegram.ext import Updater, MessageHandler
import logging
import os
import json
import sys

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
---Token/Key Management Starts---
This part will check for the config.txt file which holds the Telegram and Meetup Token/Key and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
"""
configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather."
if 'config.txt' not in os.listdir():
    with open('config.txt', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Channel-Id': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
        else:
            print(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

updater=Updater(token=TelegramBotToken)
dispatcher=updater.dispatcher

def getID(bot, update):
    print("Channel ID = " + str(update.message.chat.id) + ". Please replace this Channel ID with the value of 'Channel-ID' in config.txt.")
    sys.exit(0)

dispatcher.add_handler(MessageHandler(Filters.text, getID))

updater.start_polling()
