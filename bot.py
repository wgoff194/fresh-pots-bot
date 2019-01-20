#!/usr/bin/python
"""
Written by wbrown
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

        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
	
        self.event = event.Event(self)
        self.listen()
	
    def get_bot_id(self):
        
        self.sl_channel = self.slack_client.api_call("groups.list")['groups'][0]['id']
        self.sl_mem_codes = self.slack_client.api_call("conversations.members",channel=self.sl_channel)['members']

        for memcode in self.sl_mem_codes:
            userdata = self.slack_client.api_call("users.info",user=memcode)['user']['name']
            if userdata == 'freshpots':
                return "<@" + memcode + ">"
        
        return None
			
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected, listening for commands")
            
            if self.wallboard_url == 'none':
                self.user_in = " @here"
                print("Wallboard not specified, setting ping to:" + self.user_in)
            else:
                self.wall_chk = wallboard.wallchk(self)
                 
                if self.wall_chk == '2':
                    self.user_in = " @here"
                    print('wallboard not found, ping set to:' + self.user_in)
                else:
                    self.user_in = wallboard.active_users(self)
                    print('Wallboard found, ping currently set to:' + self.user_in)
                
            while True:
                
                if self.wall_chk == '1':
                    
                    if self.refresh_users == 3600:
                        self.refresh_users = 0
                        self.user_in = wallboard.active_users(self)
                        print(self.user_in)
                    
                    self.refresh_users += 1
                
            self.event.wait_for_event()
            time.sleep(1)
        else:
            exit("Error, Connection Failed")
