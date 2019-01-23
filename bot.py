##
# Written by wbown
##

# Python Main Imports
import os, requests, time, json, urllib, threading
from slackclient import SlackClient
from datetime import date, timedelta
from bs4 import BeautifulSoup

# My Library Imports
import event
import wallboard


class Bot(object):
    def __init__(self):
        self.slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
        self.slack_client = SlackClient(self.slack_bot_token)
        self.wallboard_url = os.environ["WALLBOARD_URL"]
        self.bot_name = "freshpots"
        self.bot_id = self.get_bot_id()
        self.user_in = ''
        self.wall_chk = '0'
        self.refresh_users = 0
        self.tags=['!fp','!freshpots']

        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
	
        self.event = event.Event(self)
        self.listen()
	
    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
            
                if 'name' in user and user.get('name') == self.bot_name:
                    return "<@" + user.get('id') + ">"
            
        return None
			
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected, listening for commands")
            while True:
                self.event.wait_for_event()
                time.sleep(1)
            else:
                exit("Error, Connection Failed")
