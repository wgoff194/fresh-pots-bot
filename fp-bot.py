#!/usr/bin/python``
"""
Written by wbrown
Importing the nessecary modules:
'requests' to make the httpd request for the URL.
"""
import os, requests, time, json
from slackclient import SlackClient
from datetime import date, timedelta
from bs4 import BeautifulSoup

"""
Set Slack Token and Client
"""

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(SLACK_BOT_TOKEN)
coffeebot_id = None

"""
Set constants
"""

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "!fp last"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

"""
Set Classes
"""

def active_users():
    """

    """
    user_in = []
    chanlist = sc.api_call("groups.list")
    print(chanlist['groups'][0]['id'])
#    for i in range(0, len(chanlist['channels'])):
        #if print(chanlist['channels'][i]['name']) == 'illumilatte':
        #    print(chanlist['channels'][i]['id'])
        #print

"""    request = sc.api_call("users.list")
    if request['ok']:
        for sl_user in request['members']:
        #    print(sl_user['name'])
            
            if sl_user['name'] !=  'slackbot':
                url = "https://wallboard.supportdev.liquidweb.com/api/data/agents/" + sl_user['name']
                html = requests.get(url)
                text = html.text
                text = text.split('"')
                end = len(text)
                if html.status_code != 200:
                    raise requests.ConnectionError("Expected status code 200, but got {}".format(page.status_code))
                for i in range(0, end):
                    if text[i] == 'punched':
                        if int(i + int(2)) == 'true':
                            user_in.append('@' + sl_user['name'])
            
"""
def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == coffeebot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith('!fp'):
        #if command == "!fp new":

        response = "Thank you for the test"

    # Sends the response back to the channel
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

#  Main Process

if __name__ == "__main__":
    if sc.rtm_connect(with_team_state=False):
        print("Fresh-Pots Bot connected and running!")
         
        refresh_users = 0
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = sc.api_call("auth.test")["user_id"]
        while True:
            if refresh_users == 3600:
                refresh_users = 0
            if refresh_users == 0:
                active_users()
            refresh_users += 1
        #    print(user_in)
            command, channel = parse_bot_commands(sc.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
