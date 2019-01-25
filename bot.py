###
# Written by Warren Brown
# Fresh-Pots Bot
# Version 1.0
##

# Python Main Imports
import os, requests, time, json, urllib, threading, pickle
from slackclient import SlackClient
from datetime import date, timedelta
from bs4 import BeautifulSoup

# My Library Imports
import event

# Create bot object 
class Bot(object):
    # Initialize bot variable and set
    def __init__(self):
        # Read token for bot
        self.slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
        # Set variable in which the api is called
        self.slack_client = SlackClient(self.slack_bot_token)
        # Set variable for bot name
        self.bot_name = "freshpots"
        # Get bot id
        self.bot_id = self.get_bot_id()
        # Set tags 
        self.tags=['!fp','!freshpots']
        # Set datapool
        self.datapool={}
        # Check if bot exists 
        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
	# Set event handler 
        self.event = event.Event(self)
        # call listen
        self.listen()
	
    # Define function to check for bot in list of user in channel 
    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find the bot
            users = api_call.get('members')
            for user in users:
            
                if 'name' in user and user.get('name') == self.bot_name:
                    return "<@" + user.get('id') + ">"
            
        return None
			
    # Define listening function that loops 
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected, listening for commands")

            with open('freshpots.pkl', 'rb') as fp:
                self.datapool = pickle.load(fp)
            fp.close() 

            while True:
                self.event.wait_for_event()
                time.sleep(1)
            else:
                exit("Error, Connection Failed")
