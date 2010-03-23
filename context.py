from netsource import Network
from functools import partial
from time import sleep


class State(dict):
	"Main Magellan class, holding the status of the active contexts and rules"
	
	def __new__(cls, *p, **k):
		if not '_singleton' in cls.__dict__:
			cls._singleton = dict.__new__(cls)
		return cls._singleton
	
	def __init__(self):
		self.current_context = self['Default']
		self.THRESHOLD = 0.6
			
	def __getitem__(self,key):
		try:
			return dict.__getitem__(self,key)
		except KeyError: #used to avoid explicitly creating a new Context object each time
			new_context = State.Context(self)
			self[key] = new_context
			return new_context
	
	def checkmax(self):
		"Select the more likely context based on the rules, and executes its input and output actions if needed"
		max_context = max(self.values(), key= lambda m:m.score)
		if True:#max_context is not self.current_context:
			if max_context.score < self.THRESHOLD: 
				if self.current_context is self['Default']:
					return #if the max_context changed but both the old and the new one where under the threshold it's useless to do any action
				max_context = self['Default']

			for action in self.current_context.out_actions:
				action()
			self.current_context = max_context
			for action in self.current_context.in_actions:
				action()

	def add_rule(self,source,value,context,confidence):
		"Add a rule to its context's rules and connects it to the event source"
		rule = partial(State.Rule(confidence),self[context],value)
		self[context].rules.append((source,rule))
		source(rule)
	
		
	class Context(object):
		"Context class: holds its current score, and the rules and actions related to this context"
		def __init__(self, state):
			self.__dict__['score'] = None
			self.rules = []
			self.in_actions = []
			self.out_actions = []
			self._state = state
		def __setattr__(self,name,value):
			self.__dict__[name]=value
			if name == 'score':
				self._state.checkmax() #every time the score is updated the most likely context is recalculated, but now the score is updated only in one place, so it's not very useful
		def update_score(self):
			"Update this context score based on individual rules confidences:\nscore= 1-((1-val1)*(1-val2)*(1-val3)...)"
			self.score = 1-reduce(float.__mul__,(1-rule.func.confidence for source,rule in self.rules if rule.func.match),1.0)
	
	
	class Rule(object):
		"Rule class: keeps trace of its confidence value and the current state (matched or not)\nif called checks if the state changed and, if so, prompts the context to update its score"
		def __init__(self,confidence):
			self.match = False
			self.confidence = confidence
		def __call__(self,context,value,values):
			match = value in values
			if self.match is not match:
				self.match = match
				context.update_score()


def in_casa():
	print "sono a casa"
	
def out_casa():
	print "esco di casa"
	
def default():
	print "contesto di default"

if __name__ == '__main__':
	network=Network()
	state = State()
	state['Casa'].in_actions.append(in_casa)
	state.add_rule(network.connect_ssid,'wlan-ap','Casa',0.8)
	state['Casa'].out_actions.append(out_casa)
	state['Default'].in_actions.append(default)
	while True:
		sleep(10)
