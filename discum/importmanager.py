#to speed up importing discum
class Imports: #method factory (https://stackoverflow.com/a/55618155)
	__slots__ = ['imports']
	def __init__(self, imports):
		self.imports = imports
	def __getattr__(self, name):
		if name in self.imports:
			def func(*args, **kwargs):
				try:
					return globals()[name](*args, **kwargs)
				except:
					globals()[name] = getattr(__import__(self.imports[name], fromlist=[name]), name)
					return globals()[name](*args, **kwargs)

			func.__name__ = name
			try:
				func.__qualname__ = __class__.__qualname__ + '.' + name
			except: #python 2
				pass
			return func