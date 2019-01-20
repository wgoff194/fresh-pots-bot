class Command(object):
	def __init__(self):
		self.commands = { 
			"test" : self.test,
			"help" : self.help
		}

	def handle_command(self, user, command):
		response = "<@" + user + ">: "
	
		if command in self.commands:
			response += self.commands[command]()
		else:
			response += "Sorry I don't understand the command: " + command + ". " + self.help()
		
		return response
		
	def test(self):
		return "Test has been successful!"
	
	def help(self):
		response = "Currently I support the following commands:\r\n"
		
		for command in self.commands:
			response += command + "\r\n"
			
		return response
