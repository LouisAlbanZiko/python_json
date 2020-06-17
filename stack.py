class Stack(list):
	def __init__(self):
		super().__init__()
	
	def push(self, element):
		self.append(element)
	
	def pop(self):
		return super().pop(len(self) - 1)
	
	def peek(self):
		return self[-1]

	def join(self, string):
		s = ""
		for e in self:
			s += e + string
		return s[0:len(s) - len(string)]