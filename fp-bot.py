#!/usr/bin/python
#
# Written by wbrown
#  Importing the nessecary modules: 
#   'requests' to make the httpd request for the URL.
#

from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

#  Setting up the list of users:
#   This will pull a list of users from channel in slack
#   For testing I am just setting a userlist



#
#  Getting the sites data:
#   This calls an internal site so this will need to be ran on Liquid Web's network.
#   Pulling admin data.
#   In this case, it's mine.
#   Also ensures HTTP response is 200 before proceeding:
#
url = "https://wallboard.supportdev.liquidweb.com/api/data/agents"
html = requests.get(url)
text = html.text
text = text.split('"')
end = len(text)

if html.status_code != 200:
    raise requests.ConnectionError("Expected status code 200, but got {}".format(page.status_code))

#
# Here's the magic:
#  Loop through the lines of the URL and if a ticket status is found as 'work_in_progress',
#  pull the status, ticket number, and subject number.
#  Makes it pretty!
#
counter = 0

for i in range(0, end):
    if text[i] == 'punched' and text[i+2] == 'true':
        hit = i
        sta = int(hit)
        tix = int(int(hit) + int(8))
        sub = int(int(hit) + int(18))
        words ="Ticket: " + text[tix] + " | Subject: " + text[sub] + " "
        if counter % 2 == 0:
            print(colors.bg.red,words)
        else:
            print(colors.bg.black,words)
#        print(colors.reset,"------------------")
        counter += 1
