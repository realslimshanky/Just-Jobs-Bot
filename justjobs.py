import inspect
import re
import signal
import subprocess
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import logging
import json
import sys
import os
from telegram import ChatAction, ParseMode, Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will save the process id of the program going in background in a file named 'pid'. Now, when you run you program again, the last one will be terminated with the help of pid. If in case the no process exist with given process id, simply the `pid` file will be deleted and a new one with current pid will be created.
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            print("Terminating previous instance of " +
                  os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token Management Starts---
This part will check for the config.json file which holds the Telegram and Channel ID and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
"""
configError = "Please open config.json file located in the project directory and replace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather."
if 'config.json' not in os.listdir():
    with open('config.json', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Channel-Id': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.json', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
            if config["Channel-Id"]:
                ChannelId = config["Channel-Id"]
            else:
                    print("Channel ID is not present in config.json. Please follow instruction on README.md, run getid.py and replace the Channel ID you obtain.")
        else:
            print(configError)
            sys.exit(0)
"""
---Token Management Ends---
"""

jobs = {}

updater = Updater(token=TelegramBotToken)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    start_msg = inspect.cleandoc('''
    Hi there! To submit a job, use /submit
    Use /help to get help''')
    update.message.reply_text(start_msg)

def help(update: Update, context: CallbackContext):
    tg_msg = inspect.cleandoc(''' 
    Use /submit to submit a job. \n
    After your submission the job will be displayed on @justjobs channel like the one below:\n
    `Company Name: XYZ Inc.
    Job Designation: Dev Ops Developer
    Job Description: https://link-to-description.html
    Qualification Needed: B.Tech
    Experience Needed: 1 year using python, HTML, CSS 
    Joining Date: September 2017
    Last Date to Apply: August 31st, 2017
    Salary Offered - 1,00,000K
    Contact Person - Mr. Kumar
    Email Id - some@thing.xyz
    Phone No - 0123456789` \n
    To report a bug or contribute to this bot visit https://github.com/Daksh777/justjobs
    ''')
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=tg_msg)

def submitJob(update: Update, context: CallbackContext):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    jobs[update.message.chat_id] = []
    context.bot.send_message(chat_id=update.message.chat_id, text="After submission, the job will be displayed on @justjobs channel")
    context.bot.send_message(chat_id=update.message.chat_id, text="What is your company name?")

def AddDetails(update: Update, context: CallbackContext):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if update.message != None and update.message.chat_id in jobs.keys():
        if len(jobs[update.message.chat_id]) == 0:
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is your job designation?")
        elif len(jobs[update.message.chat_id]) == 1:
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is your job description?")
        elif len(jobs[update.message.chat_id]) == 2:        
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What are the qualifications needed?")
        elif len(jobs[update.message.chat_id]) == 3:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is the experience needed?")
        elif len(jobs[update.message.chat_id]) == 4:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is the joining date?")
        elif len(jobs[update.message.chat_id]) == 5:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is the last date to apply?")
        elif len(jobs[update.message.chat_id]) == 6:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is the salary offered?")
        elif len(jobs[update.message.chat_id]) == 7:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="Who is the contact person?")
        elif len(jobs[update.message.chat_id]) == 8:    
            jobs[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="What is your email id?")
        elif len(jobs[update.message.chat_id]) == 9:    
            jobs[update.message.chat_id].append(update.message.text)
            if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', jobs[update.message.chat_id][9]):
                context.bot.send_message(chat_id=update.message.chat_id, text="What is your phone number?")
            else:
                context.bot.send_message(chat_id=update.message.chat_id, text="Please enter a valid email address")
        elif len(jobs[update.message.chat_id]) == 10:  
            if re.fullmatch(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', update.message.text):
                jobs[update.message.chat_id].append(update.message.text)
                tg_job_msg = inspect.cleandoc('''
                    *Company Name:* ''' + jobs[update.message.chat_id][0] + '''
                    *Job Description:* ''' + jobs[update.message.chat_id][2] + '''
                    *Job Designation:* ''' + jobs[update.message.chat_id][1] + '''
                    *Qualification Needed:* ''' + jobs[update.message.chat_id][3] + '''
                    *Experience Needed:* ''' + jobs[update.message.chat_id][4] + '''
                    *Joining Date:* ''' + jobs[update.message.chat_id][5] + '''
                    *Last Date to Connect:* ''' + jobs[update.message.chat_id][6] + '''
                    *Salary Offered:* ''' + jobs[update.message.chat_id][7] + '''
                    *Contact Person:* ''' + jobs[update.message.chat_id][8] +'''
                    *Email Id:* ''' + jobs[update.message.chat_id][9] +'''
                    *Phone No:* ''' + jobs[update.message.chat_id][10])
                context.bot.send_message(chat_id=ChannelId, text=tg_job_msg, parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(chat_id=update.message.chat_id,text='''Your Job has been posted to @justjobs''')
            else:
                context.bot.send_message(chat_id=update.message.chat_id,text='''Please enter valid phone number''')
    elif update.message.chat.type == 'private':
        context.bot.send_message(chat_id=update.message.chat_id,text='''Please use /submit to submit jobs''')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('submit', submitJob))
dispatcher.add_handler(MessageHandler(Filters.text, AddDetails))

updater.start_polling()