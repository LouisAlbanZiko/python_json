from json import parse, stringify, JSONObject
from time import time
from math import log10

# simple test for the parse function on the data.json file
obj = parse(open("data.json", "r").read())
print(stringify(obj))

# time complexity test
for i in range(10):				# run 10 tests
	obj = JSONObject()
	for nr in range((i) * 20):	# create i * 10 variables in the object
		obj.add(str(nr), nr)
	string = stringify(obj)
	start = time()				# measure time
	obj = parse(string)
	end = time()
	t = (end - start) * 1000000	# convert to nanoseconds
	string_length = len(string)
	print("{0}{1}: {2}{3:4.2f}ns".format(" " * int(4 - log10(string_length)), string_length, " " * int(4 - log10(t)), t))	# show results
