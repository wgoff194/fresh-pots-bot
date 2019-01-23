class Command(object):
	def __init__(self):
		self.commands = { 
			"test" : self.test,
			"help" : self.help
		}

	def handle_command(self, user, command,channel,request,string):
		response = "<@" + user + ">: "
	
		if command in self.commands:
			response += self.commands[command]()
		else:
			response += "Sorry I don't understand the command"
		
		return response
		
	def test(self):
		return "Test Complete"
	
	def help(self):
		response = "Currently I support the following commands:\r\n"
		
		for command in self.commands:
			response += command + "\r\n"
			
		return response
