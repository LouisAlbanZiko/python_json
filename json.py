from stack import Stack

string = ""
index = 0
line = 1
stack = Stack()

# external function to turn a string to a json object
def parse(str_arg):
	global string
	global index
	string = str_arg		# initialize variables
	index = 0
	line = 1
	return parseValue()		# parse root variable

# external function to turn the object to a string
# this was mostly used for debugging and wasn't explained in the project
def stringify(obj, indent=0):
	if isinstance(obj, JSONObject) or isinstance(obj, JSONArray):	# add indent to containers
		return obj.__str__(indent+1)
	elif isinstance(obj, str):	# add quotes to strings
		return '"'+obj+'"'
	else:
		return str(obj)			# otherwise just turn into a string

class JSONObject:
	def __init__(self):
		self.data = []
		self.names = []

	def add(self, name, value):
		self.data.append(value)
		self.names.append(name)

	def __len__(self):
		return len(self.data)
	
	# [] operator function
	# can be used as follows:
	# obj["name"]
	def __getitem__(self, name):
		index = 0
		while name != self.names[index]: # find index of name
			nextChar()
			if index == len(self.data):	 # if index is bigger than length
				raise Exception("No such item in object")	# index out of bounds
		return self.data[index]

	def __str__(self, indent=0): # function for printing
		print_string = "\n"+("\t" * (indent - 1))+"{\n" # start the object
		for i in range(len(self.data)): # for each element
			data = stringify(self.data[i], indent)	# stringify the value
			print_string += "{0}{1} : {2}{3}\n".format("\t" * indent, '"'+self.names[i]+'"', data, "," if i != len(self.data) - 1 else "") # format the name and value
		print_string += ("\t" * (indent - 1)) + "}" # end the object
		return print_string

class JSONArray(list):
	def __init__(self):
		super().__init__()

	def __str__(self, indent=0): # function for printing
		print_string = "\n"+("\t" * (indent - 1))+"[\n" # start the array
		for i in range(len(self)):	# for each element
			data = stringify(self.__getitem__(i), indent) # stringify the value
			print_string += "{0}{1}{2}\n".format("\t" * indent, data, "," if i != len(self) - 1 else "") # format the value
		print_string += ("\t" * (indent - 1)) + "]" # end the array
		return print_string

# returns a string containing info about the current state of parsing
# used to print additional information when an exception is raised
# namely the line and the variable the exception occurred on
def getInfo():
	return '\nLine: {0}, Variable: "{1}"'.format(line, stack.join('.'))

# general exception for json
# calls getInfo to print extra info about the circumstances of the exception
class JSONException(Exception):
	def __init__(self, message):
		super().__init__(message+getInfo())

def nextChar():
	global index
	global string
	global line
	if string[index] == '\n':
		line += 1
	index += 1

def skipWhitespace():
	global string
	global index
	c = string[index]
	while c == ' ' or c == '\r' or c == '\n' or c == '\t':
		nextChar()
		c = string[index]


# the following functions follow the rules explained in the word doc


# check what the type of the value is and parse using the corresponding function
def parseValue():
	global string
	global index
	skipWhitespace()
	c = string[index]
	if c == '{':
		return parseObject()
	elif c == '[':
		return parseArray()
	elif c == '"':
		return parseString()
	elif c.isdigit() or c == '-':
		return parseNr()
	elif c == 't' or c == 'f':
		return parseBool()
	else:
		raise JSONException("No value found")

def parseName():
	global string
	global index
	skipWhitespace()
	if string[index] == '"':
		nextChar()
		start = index
		while string[index] != '"':
			nextChar()
		nextChar()
		return string[start:index - 1]
	else:
		raise JSONException('Expected " for variable name')

def parseObject():
	global string
	global index
	obj = JSONObject()
	while 1:
		nextChar()
		skipWhitespace()
		if string[index] == '}':
			break
		name = parseName()
		stack.push(name)
		skipWhitespace()
		if string[index] == ':':
			nextChar()
			value = parseValue()
			obj.add(name, value)
		else:
			raise JSONException("Expected : between variable name and value")
		skipWhitespace()
		if string[index] == ',':
			stack.pop()
			continue
		elif string[index] == '}':
			stack.pop()
			break
		else:
			raise JSONException("Expected , for next variable or } for end of object")
	nextChar()
	return obj

def parseArray():
	global string
	global index
	arr = JSONArray()
	while 1:
		nextChar()
		arr.append(parseValue())
		skipWhitespace()
		if string[index] == ',':
			continue
		elif string[index] == ']':
			break
		else:
			raise JSONException("Expected , for next variable or ] for end of array")
	nextChar()
	return arr

def parseString():
	global string
	global index
	nextChar()
	start = index
	while string[index] != '"':
		nextChar()
	nextChar()
	return string[start:index - 1]

def parseNr():
	global string
	global index
	start = index
	if string[index] == '-':
		nextChar()
	while string[index].isdigit():
		nextChar()
	if string[index] != '.':
		return int(string[start:index])
	else:
		nextChar()
		while string[index].isdigit():
			nextChar()
		return float(string[start:index])

def parseBool():
	global string
	global index
	start = index
	while(string[index].isalpha()):
		nextChar()
	found_str = string[start:index]
	if found_str == "true":
		return True
	elif found_str == "false":
		return False
	else:
		raise JSONException("Expected true or false but found " + found_str)
