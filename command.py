# Python Main Imports
import os, requests, time, json, urllib, threading, datetime
from slackclient import SlackClient
from bs4 import BeautifulSoup


class Command(object):
    def __init__(self, event):
        self.event = event
        self.commands = {
                "test":self.test,
                "help":self.help,
                "add":self.addcoffee,
                "new":self.newpots,
                "list":self.listcoffee,
                "rm":self.remcoffee,
                "optin":self.optin,
                "optout":self.optout,
                "ping":self.pinglist
                }

    def handle_command(self, user, command, channel, string):
        response = "<@" + user + ">: "
        
        if command in self.commands:
            response = self.commands[command](user, channel, string)
        else:
            response += "Sorry I don't understand the command, for list of command please use `help`"
		
        return response
		
    def test(self,user, channel, string):
        return "Test Complete"
    
    def help(self,user, channel, string):
        response = "Currently I support the following commands:\r\n"

        for command in self.commands:
            response += command + "\r\n"
			
        return response

    def addcoffee(self,ser, channel, string):
        if string not in self.event.bot.datapool[channel]['coffee']:
            self.event.bot.datapool[channel]['coffee'].append(string)
            response = "Thank you for adding " + string
        else:
            response = string + " is already listed"
        return response

    def writedata(self,user, channel, string):
        self.datadump=json.dumps(self.event.bot.datapool)
        
    def newpots(self,user, channel, string):
        if 'type' in self.event.bot.datapool[channel]['prevpot2']:
            self.event.bot.datapool[channel]['prevpot3']=self.event.bot.datapool[channel]['prevpot2']
        else:
            self.event.bot.datapool[channel]['prevpot3']={}

        if 'type' in self.event.bot.datapool[channel]['prevpot1']:
            self.event.bot.datapool[channel]['prevpot2']=self.event.bot.datapool[channel]['prevpot1']
        else:
            self.event.bot.datapool[channel]['prevpot2']={}

        if 'type' in self.event.bot.datapool[channel]['newpot']:
            self.event.bot.datapool[channel]['prevpot1']=self.event.bot.datapool[channel]['newpot']
        else:
            self.event.bot.datapool[channel]['prevpot1']={}

        self.event.bot.datapool[channel]['newpot']={'type':string,'time':datetime.datetime.now()}

        pinglist = pinglist(self,user, channel, string)

        response = pinglist + "\nWe have a fresh pot of " + string + "\nhttps://i.imgur.com/l10zeET.jpg"

        return response 

    def listcoffee(self,user, channel, string):
        response = "Current coffee list:\n"
        if len(self.event.bot.datapool[channel]['coffee']) >= 1:
            for item in self.event.bot.datapool[channel]['coffee']:
                response += item + "\n"
        else:
            response = "No coffee found in list"

        return response

    def optin(self,user, channel, string):
        if user not in self.event.bot.datapool[channel]['user']:
            self.event.bot.datapool[channel]['user'].append(user)
            response = " <@" + user + ">" + " has been added to ping list"
        else:
            response = " <@" + user + ">" + " was already found in opt in list"
        return response 

    def optout(self,user, channel, string):
        if user in self.event.bot.datapool[channel]['user']:
            self.event.bot.datapool[channel]['user'].remove(user)
            response = " <@" + user + ">" + " has been removed from the opt in list"
        else:
            response = " <@" + user + ">" + " was not found in opt in list"

    def optlist(self,user, channel, string):
        response = "" 
        for user in self.event.bot.datapool[channel]['user']:
            reponse += " <@" + user + ">"
        return response

    def remcoffee(self,user, channel, string):
        if sting in self.event.bot.datapool[channel]['coffee']:
            self.event.bot.datapool[channel]['coffee'].remove(string)
            response = string + "has been removed"
        else:
            response = string + " is not listed"
        return response

    def pinglist(self,user, channel, string):
        response = '' 
        for user in self.event.bot.datapool[channel]['user']:
            response += " <@" + user + ">"
        return response

    def prevlist(self,user, channel, string):
        response = self.event.bot.datapool[channel][prevpot1]['type'] + " @ " + self.event.bot.datapool[channel][prevpot1]['time'] + "\n"
        response += self.event.bot.datapool[channel][prevpot2]['type'] + " @ " + self.event.bot.datapool[channel][prevpot2]['time'] + "\n"
        response += self.event.bot.datapool[channel][prevpot3]['type'] + " @ " + self.event.bot.datapool[channel][prevpot3]['time'] + "\n"
        return response 
