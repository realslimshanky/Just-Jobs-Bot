import inspect
import json
import logging
import os
import re
import signal
import subprocess
import sys

from telegram import ChatAction, ParseMode, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
)

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will
save the process id of the program going in background in a file named 'pid'. Now, when you run you
program again, the last one will be terminated with the help of pid. If in case the no process exist
with given process id, simply the `pid` file will be deleted and a new one with current pid will be
created.
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            logging.info(f'Terminating previous instance of {os.path.realpath(__file__)}')
        except (ProcessLookupError, ValueError):
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token Management Starts---
This part will check for the config.json file which holds the Telegram and Channel ID and will also
give a user friendly message if they are invalid. New file is created if not present in the project
directory.
"""
configError = (
    'Please open config.json file located in the project directory and replace the value "0" of '
    'Telegram-Bot-Token with the Token you recieved from botfather.'
)
if 'config.json' not in os.listdir():
    with open('config.json', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Channel-Id': 0}, f)
        logging.info(configError)
        sys.exit(0)
else:
    with open('config.json', mode='r') as f:
        config = json.loads(f.read())
        if config['Telegram-Bot-Token']:
            logging.info('Token Present, continuing...')
            TelegramBotToken = config['Telegram-Bot-Token']
            if config['Channel-Id']:
                ChannelId = config['Channel-Id']
            else:
                logging.info((
                    'Channel ID is not present in config.json. Please follow instruction on '
                    'README.md, run getid.py and replace the Channel ID you obtain.'
                ))
        else:
            logging.info(configError)
            sys.exit(0)
"""
---Token Management Ends---
"""

jobs_queue = {}

updater = Updater(token=TelegramBotToken)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    start_msg = inspect.cleandoc((
        'Hi there! To submit a job, use /submit'
        'Use /help to get help'
    ))
    update.message.reply_text(start_msg)


def botHelp(update: Update, context: CallbackContext):
    help_msg = inspect.cleandoc((
        'Use /submit to submit a job. \n'
        'After your submission the job will be displayed on @justjobs channel like the one below:\n'
        '\n`Company Name: XYZ Inc.\n'
        'Job Designation: Dev Ops Developer\n'
        'Job Description: https://link-to-description.html\n'
        'Qualification Needed: B.Tech\n'
        'Experience Needed: 1 year using python, HTML, CSS\n'
        'Joining Date: September 2017\n'
        'Last Date to Apply: August 31st, 2017\n'
        'Salary Offered - 1,00,000K\n'
        'Contact Person - Mr. Kumar\n'
        'Email Id - some@thing.xyz\n'
        'Phone No - 0123456789` \n\n'
        'To report a bug or contribute to this bot visit '
        'https://github.com/realslimshanky/Just-Jobs-Bot'
    ))
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(
        chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=help_msg,
    )


def submitJob(update: Update, context: CallbackContext):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    jobs_queue[update.message.chat_id] = []
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='After submission, the job will be displayed on @justjobs channel.',
    )
    context.bot.send_message(chat_id=update.message.chat_id, text='What is your company name?')


def addDetails(update: Update, context: CallbackContext):  # noqa: CCR001
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if update.message is not None and update.message.chat_id in jobs_queue:
        if len(jobs_queue[update.message.chat_id]) == 0:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is your job designation?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 1:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is your job description?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 2:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What are the qualifications needed?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 3:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is the experience needed?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 4:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is the joining date?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 5:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is the last date to apply?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 6:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='What is the salary offered?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 7:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(
                chat_id=update.message.chat_id, text='Who is the contact person?',
            )
        elif len(jobs_queue[update.message.chat_id]) == 8:
            jobs_queue[update.message.chat_id].append(update.message.text)
            context.bot.send_message(chat_id=update.message.chat_id, text='What is your email id?')
        elif len(jobs_queue[update.message.chat_id]) == 9:
            if re.fullmatch(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', update.message.text,
            ):
                jobs_queue[update.message.chat_id].append(update.message.text)
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text='What is your phone number? (reply "skip" to skip this question)',
                )
            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id, text='Please enter a valid email address.',
                )
        elif len(jobs_queue[update.message.chat_id]) == 10:
            PHONE_NO_REGEX = (
                r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??'
                r'\d{4})'
            )
            if re.fullmatch(
                PHONE_NO_REGEX,
                update.message.text,
            ):
                jobs_queue[update.message.chat_id].append(update.message.text)
            elif update.message.text != 'skip':
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Please enter valid phone number or reply "skip" to skip this question.',
                )
                return

            phone_number = jobs_queue[update.message.chat_id][10] if len(
                jobs_queue[update.message.chat_id]) == 11 else '(not submitted)'
            tg_job_msg = inspect.cleandoc((
                f'*Company Name:* {jobs_queue[update.message.chat_id][0]}\n'
                f'*Job Description:* {jobs_queue[update.message.chat_id][2]}\n'
                f'*Job Designation:* {jobs_queue[update.message.chat_id][1]}\n'
                f'*Qualification Needed:* {jobs_queue[update.message.chat_id][3]}\n'
                f'*Experience Needed:* {jobs_queue[update.message.chat_id][4]}\n'
                f'*Joining Date:* {jobs_queue[update.message.chat_id][5]}\n'
                f'*Last Date to Connect:* {jobs_queue[update.message.chat_id][6]}\n'
                f'*Salary Offered:* {jobs_queue[update.message.chat_id][7]}\n'
                f'*Contact Person:* {jobs_queue[update.message.chat_id][8]}\n'
                f'*Email Id:* {jobs_queue[update.message.chat_id][9]}\n'
                f'*Phone No:* {phone_number}'
            ))
            context.bot.send_message(
                chat_id=ChannelId, text=tg_job_msg, parse_mode=ParseMode.MARKDOWN)
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text='Thank you. Your Job has been posted to @justjobs',
            )
    elif update.message.chat.type == 'private':
        context.bot.send_message(
            chat_id=update.message.chat_id, text='Please use /submit to submit jobs.',
        )


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', botHelp))
dispatcher.add_handler(CommandHandler('submit', submitJob))
dispatcher.add_handler(MessageHandler(Filters.text, addDetails))

updater.start_polling()
