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
Enter Joining Date
(e.g. First week of September or specific calender date)''')
                elif len(jobDetails[update.message.chat_id]) == 3:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Last Date to Apply
(e.g. Last week of August or specific calender date)''')
                elif len(jobDetails[update.message.chat_id]) == 4:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Salary Offered
(e.g. 3 Lakh pa)''')
                elif len(jobDetails[update.message.chat_id]) == 5:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Enter name of contact person
(e.g. Mr. Kumar)''')
                elif len(jobDetails[update.message.chat_id]) == 6:
                        jobDetails[update.message.chat_id].append(update.message.text)
                        bot.sendMessage(chat_id=update.message.chat_id,text='''
Their Email ID
(e.g. some@thing.com)''')
                elif len(jobDetails[update.message.chat_id]) == 7:
                        if re.match(r"[^@]+@[^@]+\.[^@]+", update.message.text):
                                jobDetails[update.message.chat_id].append(update.message.text)
                                bot.sendMessage(chat_id=update.message.chat_id,text='''
Their 10 Digit Phone  No
(e.g. 0123456789)''')
                        else:
                                bot.sendMessage(chat_id=update.message.chat_id,text='''Enter valid email address''')
                elif len(jobDetails[update.message.chat_id]) == 8:
                        if re.match(r"^.{10,10}$", update.message.text):
                                jobDetails[update.message.chat_id].append(update.message.text) 
                                bot.sendMessage(chat_id=config['BOT']['JustJobsChannel'], text='''
Company Name - ''' + jobDetails[update.message.chat_id][0] + '''
Job Designation - ''' + jobDetails[update.message.chat_id][1] + '''
Job Description - ''' + jobDetails[update.message.chat_id][2] + '''
Joining Date - ''' + jobDetails[update.message.chat_id][3] + '''
Last Date to Connect - ''' + jobDetails[update.message.chat_id][4] + '''
Salary Offered - ''' + jobDetails[update.message.chat_id][5] + '''
Contact Person - ''' + jobDetails[update.message.chat_id][6] +'''
Email Id - ''' + jobDetails[update.message.chat_id][7] +'''
Phone No - ''' + jobDetails[update.message.chat_id][8])
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
