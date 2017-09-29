class Storage(dict):
	"""
	a storage object is like a dict, you can use obj.foo as obj['foo']
	
	"""
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError,k:
			raise AttributeError, k
			
	def __setattr__(self, key, value):
		self[key] = value
		
	def __delattr__(self, key):
		try: 
			del self[key]
		except KeyError, k:
			raise AttributeError,k
	def __repr__(self):
		return '<Storage ' + dict.__repr__(self) + '>'
		
storage = Storage

if __name__ == "__main__":
	s1 = storage(a=1)
	print s1.a