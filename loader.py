from context import State
import actions
from time import sleep
from netsource import Network
network=Network()
import yaml
state=State()

data = yaml.load(file.read(file('config.yaml','r')))

for k in data:
	try:
		for rule in data[k]['rules']:
			try:
				source = getattr(network,rule['source'])
				state.add_rule(source,rule['value'],k,rule['confidence'])
			except TypeError:
				pass
	except TypeError:
		pass
		
	try:
		state[k].in_actions.extend(map(lambda string:getattr(actions,string),data[k]['in_actions']))
	except TypeError:
		pass
		
	try:
		state[k].out_actions.extend(map(lambda string:getattr(actions,string),data[k]['out_actions']))
	except TypeError:
		pass
		
while True:
	sleep(10)
