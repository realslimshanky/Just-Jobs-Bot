# [Just-Jobs-Bot](https://telegram.me/justjobsbot)
### Current Version - 0.6

#### Version 0.1 - 23rd August 2017

*   Initial skeleton of bot can now respond to three commands.
    *   /start - initial command to start communicating with the bot
    *   /help - to get help, report bug and contribute
    *   /submit - to submit job openings


#### Version 0.2 - 24th August 2017

*   A seperate file `getid.py` added to help user get the unique ID of their channel

*   Guidelines have been added on README.md about below points
    *   How to use
    *   How to deploy your instance of this bot
    *   How to contribute

#### Version 0.3 - 17th December 2017

*   Pipenv support added to the bot.
*   Process ID management added to the bot which will help while running background instances of the bot.
*   Token management added to the bot which will help segregate the tokens from bot and provide a user friendly way of managing them.
*   `getpid.py` also supports Token management now.

#### Version 0.4 - 29th December 2017

* Questions regarding educational qualifications added to the bot.
* Fixing dependency version in `requirement.txt`
* minor bug fixes

#### Version 0.5 - 29 June 2022
* Migrate the bot to python-telegram-bot v13
* Fix dependency version in `requirements.txt`
* Fix GetID
* Use JSON config instead of txt config
* Remove unused imports and other code cleanup

#### Version 0.6 - 22 July 2022
* Adding an option to skip phone number in justjobs.py
* Removing pipenv usage
* Adding development dependencies
* Adding Flake8
