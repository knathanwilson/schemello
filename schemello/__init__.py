import re

bracket_key = '{0}(.*?){0}'
singleline_key = '(\s+{0}\s+([^\n]+)\n)'
body_key = '((\t*){0}\s+([^\n]+)\n)'

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
						out = out.replace(full, self.func(full, find, out, **args))
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
					for find in get: out = out.replace(full, self.func(full, value.strip(), out, **args))
					return out
				else: return text
		return singleline_wrapper(func)
		
	def singleline (this, word):
		def wrap (func): return this._singleline(word, func)
		return wrap
	
	def _body (this, word, func):
		class body_wrapper:
			def __init__ (self, func):
				self.func = func
				self.word = word
				self.key = body_key.format(word)
				this.mods.append(self)
			def progress (self, text, **args): return len(re.findall(self.key, text)) == 0
			def do (self, text, **args):
				get = re.findall(self.key, text)
				if get:
					full, tabs, value = get[0]
					tabs += '\t'
					scope = ''
					move = text.rfind(full) + len(full)
					replace = full
					remain = text[move:].split('\n')
					for line in remain:
						if line.startswith(tabs):
							replace += line + '\n'
							scope += line[len(tabs):] + '\n'
							move += len(line) + 1
						else: break
					rest = text[move:]
					out = text
					for find in get: out = out.replace(replace, self.func(value, scope, out, **args))
					return out
				else: return text
		return body_wrapper(func)
	
	def body (this, word):
		def wrap (func): return this._body(word, func)
		return wrap
	
	def _pattern (this, key, func):
		class pattern_wrapper:
			def __init__ (self, func):
				self.func = func
				self.key = key
				this.mods.append(self)
			def progress (self, text, **args): return len(re.findall(self.key, text)) == 0
			def do (self, text, **args):
				out = text
				get = re.findall(self.key, text)
				for key in get:
					full, word = key
					out = out.replace(full, self.func(word, text, **args))
				return out
		return pattern_wrapper(func)
	
	def pattern (this, word):
		def wrap (func): return this._pattern(word, func)
		return wrap

class scheme:
	
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
	
	def body (this, word):
		def wrap (func): return this._basestage()._body(word, func)
		return wrap
