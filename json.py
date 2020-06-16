class JSONObject:
	def __init__(self):
		self.data = []
		self.names = []

	def add(self, name, value):
		self.data.append(value)
		self.names.append(name)

	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, name): # [] operator function
		index = 0
		while name != self.names[index]: # find index of name
			index += 1
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

string = ""
index = 0

# function to turn the the object to a string
def stringify(obj, indent=0):
	if isinstance(obj, JSONObject) or isinstance(obj, JSONArray):
		return obj.__str__(indent+1)
	elif isinstance(obj, str):
		return '"'+obj+'"'
	else:
		return str(obj)

# function to turn a string to a json object
def parse(str_arg):
	global string
	global index
	string = str_arg
	index = 0
	return parseValue()

def skipWhitespace():
	global string
	global index
	c = string[index]
	while c == ' ' or c == '\r' or c == '\n' or c == '\t':
		index += 1
		c = string[index]

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
	elif c.isdigit():
		return parseNr()
	elif c == 't' or c == 'f':
		return parseBool()
	else:
		pass

def parseName():
	global string
	global index
	skipWhitespace()
	if string[index] == '"':
		index += 1
		start = index
		while string[index] != '"':
			index += 1
		index += 1
		return string[start:index - 1]
	else:
		raise Exception('Expected " for variable name')

def parseObject():
	global string
	global index
	obj = JSONObject()
	while 1:
		index += 1
		name = parseName()
		skipWhitespace()
		if string[index] == ':':
			index += 1
			value = parseValue()
			obj.add(name, value)
		else:
			raise Exception("Expected : between variable name and value")
		skipWhitespace()
		if string[index] == ',':
			continue
		elif string[index] == '}':
			break
		else:
			raise Exception("Expected , for next variable or } for end of object")
	index += 1
	return obj

def parseArray():
	global string
	global index
	arr = JSONArray()
	while 1:
		index += 1
		arr.append(parseValue())
		skipWhitespace()
		if string[index] == ',':
			continue
		elif string[index] == ']':
			break
		else:
			raise Exception("Expected , for next variable or ] for end of array")
	index += 1
	return arr

def parseString():
	global string
	global index
	index += 1
	start = index
	while string[index] != '"':
		index += 1
	index += 1
	return string[start:index - 1]

def parseNr():
	global string
	global index
	start = index
	while string[index].isdigit():
		index += 1
	if string[index] != '.':
		return int(string[start:index])
	else:
		index += 1
		while string[index].isdigit():
			index += 1
		return float(string[start:index])

def parseBool():
	global string
	global index
	start = index
	while(string[index].isalpha()):
		index += 1
	found_str = string[start:index]
	if found_str == "true":
		return True
	elif found_str == "false":
		return False
	else:
		raise Exception("Expected true or false but found " + found_str)



