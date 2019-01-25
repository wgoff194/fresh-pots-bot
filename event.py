###
# Written by Warren Brown
# Fresh-Pots Bot
# Version 1.0
##

# My Imports
import command

# Create class
class Event:
    # Initialize object values
    def __init__(self, bot):
        # Set bot data into local data 
        self.bot = bot
        self.command = command.Command(self)

    # Define function to wait for event data
    def wait_for_event(self):
        # Listen to Slack Event API
        events = self.bot.slack_client.rtm_read()
        # If event has data	
        if events and len(events) > 0:
            # For each event, call parse_event function
            for event in events:
                self.parse_event(event)
				
    # Define parse event funtion 
    def parse_event(self, event):
        # Check if event is text type
        if event and 'text' in event:
            # Get events channel to make suer its in datapool
            chanevent = event['channel']
            # Check for channel in datapool, if not then add channel to datapool
            if chanevent not in self.bot.datapool:
                self.channel_create(chanevent)
            # Check for command flags
            if '!fp' in event['text'] or '!freshpots' in event['text']:
                # Check for what tag is in use
                if '!fp' in event['text']:
                    fphandle='!fp'
                if '!freshpots' in event['text']:
                    fphandle='!freshpots'
                # Check if command is passed after flag
                try: 
                    event['text'].split(fphandle)[1]
                except IndexError:
                    request='help me'
                else:               
                    request=event['text'].split(fphandle)[1].strip()
                try:
                    command=request.split()[0]
                except IndexError:
                    command='help'
                else:
                    command=request.split()[0]
                try:
                    string=request.split(command)[1].strip()
                except IndexError:
                    string="help"
                else:
                    string=request.split(command)[1].strip()
                # Print command and string to terminal for testing
                print("Command: " + command + " | String : " + string)
                # Call event handler 
                self.handle_event(event['user'], command.lower(), event['channel'],string)
    
    # Define function to handle events
    def handle_event(self, user, command, channel, request):
        # Make sure we have command and channel 
        if command and channel:
            # Get response from the command handler
            response = self.command.handle_command(user,command,channel,request)
            # Pass response to the Slack API
            self.bot.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    # Define function to create channel and subsets in datapool
    def channel_create(self, channel):
        self.bot.datapool[channel]={}
        self.bot.datapool[channel]['coffee']=[]
        self.bot.datapool[channel]['user']=[]
        self.bot.datapool[channel]['newpot']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot1']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot2']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot3']={'type':'','time':''}


