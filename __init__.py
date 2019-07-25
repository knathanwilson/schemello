import re

bracket_key = '{0}(.*?){0}'
singleline_key = '(\s+{0}\s+([^\n]+)\n)'

class stage:
	
	# std
	def __init__ (this): this.mods = []
	
	# functionality
	def __call__ (this, text, **args):
		
		# start
		out = text
		
		# modify
		if this.mods:
			while True:
				for mod in this.mods: out = mod.do(out, **args)
				should_break = True
				for mod in this.mods:
					if not mod.progress(out, **args):
						should_break = False
						break
				if should_break: break
				
		# finished!
		return out
	
	# decorators
	def _token (this, word, func):
		class token_wrapper:
			def __init__ (self, func):
				self.func = func
				self.word = word
				this.mods.append(self)
			def progress (self, text, **args): return self.word not in text
			def do (self, text, **args): return text.replace(self.word, self.func(text, **args))
		return token_wrapper(func)
		
	def token (this, word):
		def wrap (func): return this._token(word, func)
		return wrap
		
	def simpletoken (this, word, newword):
		class token_wrapper:
			def __init__ (self):
				self.word = word
				this.mods.append(self)
			def progress (self, text, **args): return self.word not in text
			def do (self, text, **args): return text.replace(self.word, newword)
		return token_wrapper()
	
	def _bracket (this, tag, func):
		class bracket_wrapper:
			def __init__ (self, func):
				self.func = func
				self.tag = tag
				self.key = bracket_key.format(tag)
				this.mods.append(self)
			def progress (self, text, **args): return len(re.findall(self.key, text)) == 0
			def do (self, text, **args):
				get = re.findall(self.key, text)
				if get:
					out = text
					for find in get:
						full = self.tag + find + self.tag
						out = out.replace(full, self.func(full, find, text, **args))
					return out
				else: return text
		return bracket_wrapper(func)
		
	def bracket (this, tag):
		def wrap (func): return this._bracket(tag, func)
		return wrap
		
	def _singleline (this, word, func):
		class singleline_wrapper:
			def __init__ (self, func):
				self.func = func
				self.word = word
				self.key = singleline_key.format(word)
				this.mods.append(self)
			def progress (self, text, **args): return len(re.findall(self.key, text)) == 0
			def do (self, text, **args):
				get = re.findall(self.key, text)
				if get:
					full, value = get[0]
					out = text
					for find in get: out = out.replace(full, self.func(full, value.strip(), text, **args))
					return out
				else: return text
		return singleline_wrapper(func)
		
	def singleline (this, word):
		def wrap (func): return this._singleline(word, func)
		return wrap


class schemer:
	
	def __init__ (this): this.stages = []
	
	def __call__ (this, text, **args):
		out = text
		for stage in this.stages: out = stage(text, **args)
		return out
	
	def _basestage (this):
		if len(this.stages) == 0:
			_stage = stage()
			this.stages.append(_stage)
			return _stage
		else: return this.stages[0]
	
	def token (this, word):
		def wrap (func): return this._basestage()._token(word, func)
		return wrap
	
	def simpletoken(this, word, newword): return this._basestage().simpletoken(word, newword)
	
	def bracket (this, word):
		def wrap (func): return this._basestage()._bracket(word, func)
		return wrap
	
	def singleline (this, word):
		def wrap (func): return this._basestage()._singleline(word, func)
		return wrap

s = schemer()
st = s._basestage()

@s.singleline('name')
def n  (full, line, text, **args): return 'moew'

print(s('''
name billy

name bleh

kakee
'''))
