from copy import deepcopy

class defdict(dict):
	def __init__(self,*args,**kwargs):
		if "default" in kwargs:
			self.default = kwargs["default"]
			del kwargs["default"]
		else:
			self.default = None
		super().__init__(*args,**kwargs)

	def __missing__(self,key):
		if callable(self.default):
			self[key] = self.default(key)
			return self[key]
		else:
			self[key] = self.default
			return self.default

class Memory:
	def __init__(self,default):
		self.default = default
		self.mem = dict()

	def __getitem__(self,key):
		if type(key) is tuple:
			if key[0] not in self.mem:
				self.mem[key[0]] = deepcopy(self.default)
			wk = self.mem[key[0]]
			default = self.default
			for step in key[1:]:
				if step in wk:
					wk = wk[step]
					default = default[step]
				else:
					default = default[step]
					wk[step] = deepcopy(default)
					wk = wk[step]
			return wk
		else:
			if key not in self.mem:
				self.mem[key] = deepcopy(self.default)
			return self.mem[key]

	def __setitem__(self,key,value):
		if type(key) is tuple:
			x = self.__getitem__(key[:-1])
			x[key[-1]] = value
		else:
			self.mem[key] = value

	def __contains__(self,key):
		return key in self.mem

	def load_default(self,key):
		self.mem[key] = deepcopy(self.default)

	def __len__(self):
		return len(self.mem)