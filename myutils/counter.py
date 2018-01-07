class Counter(storage):
	def add(self, n):
		self.setdefault(n, 0)
		self[n] += 1
		
	def most(self):
		m = max(self.itervalues())
		return [k for k,v in self.iteritems if v == m]
		
