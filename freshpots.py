#!/usr/bin/python``
"""
Written by wbrown
Importing the nessecary modules:
"""

###
# Import data
###


# Python Main Imports
import os, requests, time, json, urllib, threading
from slackclient import SlackClient
from datetime import date, timedelta
from bs4 import BeautifulSoup

# My Library Imports
from lib import slackapi, wallboard

###
# Set Slack Token and Client
###

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_bot_token)
coffeebot_id = None

###
# Set constants
###

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
sl_channel = sc.api_call("groups.list")['groups'][0]['id']

###
# Set variables
###

user_in=''
wall_chk= '0'

###
# Main Process
###

if __name__ == "__main__":
    if sc.rtm_connect(with_team_state=False):
        print("Fresh-Pots Bot connected and running!")
        refresh_users = 0
        wall_chk = wallboard.wallchk()
        if wall_chk == '2':
            user_in = " @here"
            print('wallboard not found, ping set to:' + user_in)
        else:
            user_in = wallboard.active_users(sc,sl_channel,user_in)
            print('Wallboard found, ping currently set to:' + user_in)
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = sc.api_call("auth.test")["user_id"]
        while True:
            if wall_chk == '1':
                if refresh_users == 3600:
                    refresh_users = 0
                    user_in = wallboard.active_users(sc,sl_channel,user_in)
                    print(user_in)
                refresh_users += 1
            command, channel = slackapi.parse_bot_commands(sc.rtm_read())
            if command:
                slackapi.handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
