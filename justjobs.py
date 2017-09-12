from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from time import sleep
import logging
import requests
import re
import os
import json
import sys
import signal
import subprocess

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
This part will check for the config.txt file which holds the Telegram and Channel ID and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
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
            if config["Channel-Id"]:
                ChannelId = config["Channel-Id"]
            else:
                    print("Channel ID is not present in config.txt. Please follow instruction on README.md, run getid.py and replace the Channel ID you obtain.")
        else:
            print(configError)
            sys.exit(0)
"""
---Token Management Ends---
"""

updater=Updater(token=TelegramBotToken)
dispatcher=updater.dispatcher

jobDetails = {}

print("I'm On..!!")

def start(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Hi! Let's begin /submit
Use /help to get /help''')

def help(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Only command you should be using is /submit
After your submission the job will be displayed on @justjobs channel like the one below
Company Name - XYZ Inc.
Job Designation - Dev Ops Developer
Job Description - https://link-to-description.html
Qualification Needed - B.Tech
Experience Needed - 1 year using python, HTML, CSS 
Joining Date - September 2017
Last Date to Apply - August 31st, 2017
Salary Offered - 1,00,000K
Contact Person - Mr. Kumar
Email Id - some@thing.xyz
Phone No - 0123456789 

To report a bug or contribute to this bot visit https://github.com/realslimshanky/Just-Jobs-Bot
''')

def submitJob(bot, update):
        global jobDetails

        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        jobDetails[update.message.chat_id] = []
        bot.sendMessage(chat_id=update.message.chat_id,text='''
After your submission the job will be displayed on @justjobs channel''')
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Company Name''')

def addDetails(bot, update):
        global jobDetails
        
        if update.message != None and update.message.chat_id in jobDetails.keys():
                if len(jobDetails[update.message.chat_id]) == 0:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Job Designation
(e.g. Front-End Developer)''')
                elif len(jobDetails[update.message.chat_id]) == 1:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Job Description
(Share links related to job detail here)''')
                elif len(jobDetails[update.message.chat_id]) == 2:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Minimum Education Qualification needed by the Employee to apply
(e.g. B.Tech,M.Tech)''')
                elif len(jobDetails[update.message.chat_id]) == 3:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Minimum Experience needed by the Employee to apply
(e.g. 3 years)''')
                elif len(jobDetails[update.message.chat_id]) == 4:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter Joining Date
(e.g. First week of September or specific calender date)''')
                elif len(jobDetails[update.message.chat_id]) == 5:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Last Date to Apply
(e.g. Last week of August or specific calender date)''')
                elif len(jobDetails[update.message.chat_id]) == 6:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Salary Offered
(e.g. 3 Lakh pa)''')
                elif len(jobDetails[update.message.chat_id]) == 7:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter name of contact person
(e.g. Mr. Kumar)''')
                elif len(jobDetails[update.message.chat_id]) == 8:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Their Email ID
(e.g. some@thing.com)''')
                elif len(jobDetails[update.message.chat_id]) == 9:
                        if re.match(r"[^@]+@[^@]+\.[^@]+", update.message.text):
                                jobDetails[update.message.chat_id].append(update.message.text)
                                bot.sendMessage(chat_id=update.message.chat_id,text='''
Their 10 Digit Phone  No
(e.g. 0123456789)''')
                elif len(jobDetails[update.message.chat_id]) == 10:
                        else:
                                bot.sendMessage(chat_id=update.message.chat_id,text='''Enter valid email address''')
                        if re.match(r"^.{10,10}$", update.message.text):
                                jobDetails[update.message.chat_id].append(update.message.text) 
                                bot.sendMessage(chat_id=ChannelId, text='''
Company Name - ''' + jobDetails[update.message.chat_id][0] + '''
Job Designation - ''' + jobDetails[update.message.chat_id][1] + '''
Job Description - ''' + jobDetails[update.message.chat_id][2] + '''
Qualification Needed - ''' + jobDetails[update.message.chat_id][3] + '''
Experience Needed - ''' + jobDetails[update.message.chat_id][4] + '''
Joining Date - ''' + jobDetails[update.message.chat_id][5] + '''
Last Date to Connect - ''' + jobDetails[update.message.chat_id][6] + '''
Salary Offered - ''' + jobDetails[update.message.chat_id][7] + '''
Contact Person - ''' + jobDetails[update.message.chat_id][8] +'''
Email Id - ''' + jobDetails[update.message.chat_id][9] +'''
Phone No - ''' + jobDetails[update.message.chat_id][10])
                                bot.sendMessage(chat_id=update.message.chat_id,text='''Your Job has been posted to @justjobs''')
                        else:
                                bot.sendMessage(chat_id=update.message.chat_id,text='''Please enter valid phone number''')
        elif update.message.chat.type == 'private':
                bot.sendMessage(chat_id=update.message.chat_id,text='''Please use /submit to submit jobs''')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('submit', submitJob))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, addDetails))

updater.start_polling()
