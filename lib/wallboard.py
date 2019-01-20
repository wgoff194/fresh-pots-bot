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

###
# Functions
### 

def active_users(sc,sl_channel,user_in):
    """
    """
    user_in = ''
    sl_mem_codes= sc.api_call("conversations.members",channel=sl_channel)['members']
    json_url = "https://wallboard.supportdev.liquidweb.com/api/data/agents/"
    try:
        conni = urllib.request.urlopen(json_url)
    except urllib.error.HTTPError as e:
        user_in = '@here'
    except urllib.error.URLError as e:
        user_in = '@here'
    else:
        for memcode in sl_mem_codes :
            userdata = sc.api_call("users.info",user=memcode)['user']['name']
            json_url = "https://wallboard.supportdev.liquidweb.com/api/data/agents/" + userdata
            try:
                conni = urllib.request.urlopen(json_url)
            except urllib.error.HTTPError as e:
                 ecode = 'HTTPError: {}'.format(e.code)
            except urllib.error.URLError as e:
                 ecode = 'URLError: {}'.format(e.reason)
            else:
                with urllib.request.urlopen(json_url) as url:
                    json_data = json.loads(url.read().decode())
                    if 'punched' in json_data:
                        user_in = user_in + ' @'+userdata
    return user_in

