###
# Written by Warren Brown 
# Fresh-Pots Bot 
# Version 1.0
##


# Python Main Imports
import os, requests, time, json, urllib, threading, datetime, pickle
from slackclient import SlackClient
from bs4 import BeautifulSoup

# Create Object 
class Command(object):

    # Initialize object values
    def __init__(self, event):
        # Set set object event data as the passed event data
        self.event = event
        # Set list of commands 
        self.commands = {
                "new":{'com':self.newpots,'desc':'Announces fresh pot and records to time'},
                "last":{'com':self.lastpot,'desc':'Info on last pot of coffee'},
                #"prev":{'com':self.prevlist,'desc':'List of previous pots of coffee'},
                "list":{'com':self.listcoffee,'desc':'Lists current coffee stock'},
                "add":{'com':self.addcoffee,'desc':'Add a coffee to list of available stock'},
                "rm":{'com':self.remcoffee,'desc':'Removes coffee from coffee stock'},
                "optin":{'com':self.optin,'desc':'Add yourself to ping list'},
                "optout":{'com':self.optout,'desc':'remove yourself from ping list'},
                "ping":{'com':self.pinglist,'desc':'Ping users on ping list'},
                "help":{'com':self.help,'desc':'Prints list of usable commands'},
                "test":{'com':self.test,'desc':'This is for testing the bot'}
                }

    # Define Function to process what command was requested 
    def handle_command(self, user, command, channel, string):
        response = "<@" + user + ">: "
        # Check if command is one of list of commands 
        if command in self.commands:
            # Pushes data to command
            response = self.commands[command]['com'](user, channel, string)
        else:
            # Responds if command is not found
            response += "Sorry I don't understand the command, for list of command please use `help`"
        # Pass data sent back from command of fail back to event object
        return response
    
    # Define function to save data after alter
    def writedata(self, user, channel, string):
        # Open file for modification 
        with open('freshpots.pkl', 'wb') as fp:
            # Dump file as Pickle 
            pickle.dump(self.event.bot.datapool, fp, protocol=pickle.HIGHEST_PROTOCOL)
        # Close file
        fp.close()
        # Return datasaved response
        response = "Data saved"
    
    # Define function for Test command
    def test(self,user, channel, string):
        # Return positive test 
        return "Test Complete"
    
    # Define help function, lists all available commands
    def help(self, user, channel, string):
        # Begin response sting
        response = "Currently I support the following commands:\r\n```"
        # Iterate through commands with descriptions
        for command in self.commands:
            response += "{:<10}".format(command) + ":  " + self.commands[command]['desc'] + "\r\n"
	# Close code block 
        response += "```"
        # Return list		
        return response
    
    # Define Function to add a coffee to list of coffees
    def addcoffee(self, user, channel, string):
        # Check if coffee is already in list
        if string not in self.event.bot.datapool[channel]['coffee']:
            # Adds coffee and set response 
            self.event.bot.datapool[channel]['coffee'].append(string)
            response = "Thank you for adding " + string
        # Return Fail response if Coffee already listed 
        else:
            response = string + " is already listed"
        # Saves datapool
        self.writedata(user, channel, string)
        # Return response 
        return response
    
    # Define function to list users that want to be pinged 
    def pinglist(self, user, channel, string):
        # set response to empty
        response = ''
        # Iterate though user codes that opted in  
        for user in self.event.bot.datapool[channel]['user']:
            response += " <@" + user + ">"
        # Return list of user
        return response

    # Define function to set name and time stamp for new pot
    # Move current into previous list moving the previous list down in a waterfall
    def newpots(self, user, channel, string):
        # Check if the second previous pot has data and move to third if found
        if 'type' in self.event.bot.datapool[channel]['prevpot2']:
            self.event.bot.datapool[channel]['prevpot3']=self.event.bot.datapool[channel]['prevpot2']
        else:
            self.event.bot.datapool[channel]['prevpot3']={}
        # Check if the first previous pot has data and move to second if found
        if 'type' in self.event.bot.datapool[channel]['prevpot1']:
            self.event.bot.datapool[channel]['prevpot2']=self.event.bot.datapool[channel]['prevpot1']
        else:
            self.event.bot.datapool[channel]['prevpot2']={}
        # Check if the last pot has data and move to first if found
        if 'type' in self.event.bot.datapool[channel]['newpot']:
            self.event.bot.datapool[channel]['prevpot1']=self.event.bot.datapool[channel]['newpot']
        else:
            self.event.bot.datapool[channel]['prevpot1']={}
        # Save current new pot and time stamp
        self.event.bot.datapool[channel]['newpot']={'type':string,'time':datetime.datetime.now()}
        # Create ping list for announcment
        ping = self.pinglist(user, channel, string)
        # Respond with ping, what was made and the Fresh Pots MEME
        response = ping + "\nWe have a fresh pot of " + string + "\nhttps://i.imgur.com/l10zeET.jpg"
        # Save datapool
        self.writedata(user, channel, string)
        # Return response 
        return response 

    # Define function to list coffees
    def listcoffee(self, user, channel, string):
        # Set initial response data
        response = "Current coffee list:\n"
        # Check coffee list data for info 
        if len(self.event.bot.datapool[channel]['coffee']) >= 1:
            # Iterate through list of coffee
            for item in self.event.bot.datapool[channel]['coffee']:
                response += item + "\n"
        # Respond is list is empty
        else:
            response = "No coffee found in list"
        # Return list or fail reply
        return response

    # Define Function for user ping opt-in
    def optin(self, user, channel, string):
        # Check if user in opt-in already
        if user not in self.event.bot.datapool[channel]['user']:
            # Add user to list and responds with affermative
            self.event.bot.datapool[channel]['user'].append(user)
            response = " <@" + user + ">" + " has been added to ping list"
        # Respond with fail
        else:
            response = " <@" + user + ">" + " was already found in opt in list"
        # Save datapool
        self.writedata(user, channel, string)
        # Return response
        return response 
    
    # Define Function for user ping opt-out
    def optout(self, user, channel, string):
        # Check if user in opt-in list
        if user in self.event.bot.datapool[channel]['user']:
            # Remove user when found and respond in affermative
            self.event.bot.datapool[channel]['user'].remove(user)
            response = " <@" + user + ">" + " has been removed from the opt in list"
        # Respond with fail
        else:
            response = " <@" + user + ">" + " was not found in opt in list"
        # Save datapool
        self.writedata(user, channel, string)
        # Return response
        return response
    
    # Define function to remove coffee from list
    def remcoffee(self, user, channel, string):
        # Check if Coffee is on the list 
        if string in self.event.bot.datapool[channel]['coffee']:
            # Remove coffee from list and set response
            self.event.bot.datapool[channel]['coffee'].remove(string)
            response = string + " has been removed"
        # Respond with fail 
        else:
            response = string + " is not listed, I recommend listing and copy pasting coffee name"
        # Save datapool
        self.writedata(user, channel, string)
        # Return Response
        return response
    
    # Define function to list previous pots
    def prevlist(self, user, channel, string):
        response = ''
        # Set respond for previous pot 1
        if 'type' in self.event.bot.datapool[channel]['prevpot1']:
            response = self.event.bot.datapool[channel]['prevpot1']['type'] + " : " + self.gettime(channel, 'prevpot1') + " ago\n"
        # Set respond for previous pot 2
        if 'type' in self.event.bot.datapool[channel]['prevpot2']:
            response += self.event.bot.datapool[channel]['prevpot2']['type'] + " : " + self.gettime(channel, 'prevpot2') + " ago\n"
        # Set respond for previous pot 3
        if 'type' in self.event.bot.datapool[channel]['prevpot3']:
            response += self.event.bot.datapool[channel]['prevpot3']['type'] + " : " + self.gettime(channel, 'prevpot3') + " ago\n"
        # Return response
        return response
    
    # Define function to get last made coffee and how long ago
    def lastpot(self, user, channel, string):
        # Set response with name and age
        response = "The last coffee, " + self.event.bot.datapool[channel]['newpot']['type'] + ", was made " + self.gettime(channel, 'newpot') + " ago"
        # Return Data
        return response
    
    # Define function to get age of pot called 
    def gettime(self, channel, potname):
        # Get difference in age
        age = datetime.datetime.now() - self.event.bot.datapool[channel][potname]['time']
        # Set difference in seconds
        s=age.total_seconds()
        # Process Math
        # hours
        hours = s // 3600 
        # remaining seconds
        s = s - (hours * 3600)
        # minutes
        minutes = s // 60
        # remaining seconds just in case
        seconds = s - (minutes * 60)
        # Set response with formatted data
        response = '{:01} hours {:01} minutes'.format(int(hours), int(minutes))
        # Return formatted data 
        return response
