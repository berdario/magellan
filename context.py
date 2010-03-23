from netsource import Network, SmartNetwork
from functools import partial

def ciao():
	print "ciao"

network=Network()
snetwork=SmartNetwork()

class State(object):
	
		
		
	class Context(object):
		def __init__(self):
			self.__dict__['score'] = None
			self.in_actions = []
			self.out_actions = []
		def __setattr__(self,name,value):
			self.__dict__[name]=value
			if name == 'score':
				State.checkmax()
	
	contexts = {'Default':Context()}
	current_context = 'Default'
	THRESHOLD = 0.6
	
	@classmethod
	def checkmax(cls):
		max_context_name=max(cls.contexts,key=lambda m:cls.contexts[m].score)
		max_context=cls.contexts[max_context_name]
		if max_context_name is not cls.current_context and max_context.score >= cls.THRESHOLD:
			print 'contesto con score piu\' alto:',max_context_name,'contesto corrente',cls.current_context,'punteggio',max_context.score
			for action in cls.contexts[cls.current_context].out_actions:
				action()
			cls.current_context = max_context_name
			for action in max_context.in_actions:
				action()
			
	contexts['Casa']=Context()
	contexts['Casa'].in_actions.append(ciao)



	@staticmethod	
	def add_rule(source,value,context,confidence):
		source(partial(State.rule,value,context,confidence))
		
	@classmethod	
	def rule(cls,value,context,confidence,ssids):
		if value in ssids:
			cls.contexts[context].score=confidence
			
	@staticmethod		
	def add_dumb(source,value,context,confidence):
		source(partial(State.dumbrule,context,confidence),value)
		
	@classmethod
	def dumbrule(cls,context,confidence):
		cls.contexts[context].score=confidence

		
		
if __name__ == '__main__':
	#State.add_rule(network.connect_ssid,'wlan-ap','Casa',0.8)
	State.add_dumb(snetwork.connect_ssid,'wlan-ap','Casa',0.8)
		
	
