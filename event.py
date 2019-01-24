import command

class Event:
    def __init__(self, bot):
        self.bot = bot
        self.command = command.Command(self)
	
    def wait_for_event(self):
        events = self.bot.slack_client.rtm_read()
		
        if events and len(events) > 0:
            for event in events:
                #print(event)
                self.parse_event(event)
				
    def parse_event(self, event):
        if event and 'text' in event:
            chanevent = event['channel']
            #print(chanevent)
            #print(self.bot.datapool)
            if chanevent not in self.bot.datapool:
                self.channel_create(chanevent)

            if '!fp' in event['text'] or '!freshpots' in event['text']:
                
                if '!fp' in event['text']:
                    fphandle='!fp'
                if '!freshpots' in event['text']:
                    fphandle='!freshpots'
                
                request=event['text'].split(fphandle)[1].strip()
                command=request.split()[0]
                string=request.split(command)[1].strip()

                print("Request: " + request + " | Command: " + command + " | String : " + string)
                self.handle_event(event['user'], command.lower(), event['channel'],string)
	
    def handle_event(self, user, command, channel, request):
        if command and channel:
            #print("Received command: " + command + " in channel: " + channel + " from user: " + user)
            response = self.command.handle_command(user,command,channel,request)
            self.bot.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


    def channel_create(self, channel):
        self.bot.datapool[channel]={}
        self.bot.datapool[channel]['coffee']=[]
        self.bot.datapool[channel]['user']=[]
        self.bot.datapool[channel]['newpot']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot1']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot2']={'type':'','time':''}
        self.bot.datapool[channel]['prevpot3']={'type':'','time':''}


