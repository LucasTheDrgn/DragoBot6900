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