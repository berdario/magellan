from state import State
import actions
from time import sleep
from netsource import NetworkSource
network = NetworkSource()
import yaml

configfile = 'config.yaml'

def loadconfig():
    state = State()
    data = yaml.safe_load(file.read(file(configfile, 'r')))

    for k in data:
        try:
            for rule in data[k]['rules']:
                try:
                    source = getattr(network, rule['source'])
                    state.add_rule(source, rule['value'], k, rule['confidence'])
                except TypeError:
                    pass
        except TypeError:
            pass
        except KeyError:
            pass
            
        try:
            state[k].in_actions.extend(map(lambda string:getattr(actions, string), data[k]['in_actions']))
        except TypeError:
            pass
            
        try:
            state[k].out_actions.extend(map(lambda string:getattr(actions, string), data[k]['out_actions']))
        except TypeError:
            pass
    return state
        
def saveconfig(state):
    data = dict()
    for key in state:
        data[key] = dict()
        if state[key].rules:
            data[key]['rules'] = []
        for source, rule in state[key].rules:
            data[key]['rules'].append({'confidence':rule.func.confidence, 'source':source.func_name, 'value':rule.args[1]})
        data[key]['in_actions'] = map(lambda action:action.func_name, state[key].in_actions)
        data[key]['out_actions'] = map(lambda action:action.func_name, state[key].out_actions)
        
    yaml.safe_dump(data, stream=file(configfile, 'w'), default_flow_style=False)

