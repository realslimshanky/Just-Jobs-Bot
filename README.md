# [Just-Jobs-Bot](https://telegram.me/justjobsbot)
### Current Version - 0.6 [![Build Status](https://travis-ci.org/realslimshanky/Just-Jobs-Bot.svg?branch=master)](https://travis-ci.org/realslimshanky/Just-Jobs-Bot) ([see change logs](https://github.com/realslimshanky/Just-Jobs-Bot/blob/master/ChangeLogs.md))
Just Jobs Bot is a telegram bot which gathers detail of job opening from employer and post on the Just Jobs Channel.

## How To Use

To use the bot you simply have to send below mentioned commands as text message.

/start - initial command to begin talking to the bot

/help - to get help, report bug and contribute

/submit - to submit job opening in your company

The sole purpose of this bot is to get following details from the employer about the job opening.
* Company Name - This is the full name of the company
* Job Designation - Position for which this job opening is all about
* Job Description - Little detail about the job which can be also a link to document
* Joining Date - Date from when the employee's term starts
* Last Date to Apply - Date upto which a person can apply for this job
* Salary Offered - Expected salary, can also be a range.
* Contact Person - Person whom one should contact if interested
* Email ID - Email of the contact person
* Phone Number (optional, can be 'skip'ped) - Phone number of the contact person

## How To Deploy Your Instance Of This Bot

You need Python 3 (recommended version 3.9+) and PIP installed for this to work
* Fork the repo to your profile
* `git clone link-to-repo.git` - Clone your copy of this repo to your local machine
* `cd Just-Jobs-Bot` - Move to the repo folder
* Create a virtual environment using `python -m venv venv`
* Activate virtual environment using `source venv/bin/activate`
* `pip install -r requirements-dev.txt` - install dependencies
* Create a new bot using [Botfather](https://telegram.me/botfather)
* Replace `Telegram-Bot-Token` with the token you get from Botfather in `config.json` file
* Create a channel and make it public to get the username e.g. @mychannel
* We need unique ID of this channel, to get that first add your bot as administrator to the channel you just created
* Run `python getid.py` and send `test` to the channel
* The channel ID will be logged onto the terminal
* Replace this unique ID with `Channel-Id` in `config.json` file
* Now run `python justjobs.py`
* You can now use commands mentioned above in `How To Use` section

## How To Contribute

* Create an issue in case you find one with the bot. Please mention how you got to that issue in brief.
* Fork this repo and create a feature/bug branch and make your changes to that.
* Create PR from feature/bug branch to master of this repo.
