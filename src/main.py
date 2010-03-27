# -*- coding: utf-8 -*-

import loader
from time import sleep

if __name__ == '__main__':
    #network=Network()
    #state = State()
    state = loader.loadconfig()
    loader.saveconfig(state)
    #state['Casa'].in_actions.append(in_casa)
    #state.add_rule(network.connect_ssid,'wlan-ap','Casa',0.8)
    # state.add_rule(SSIDRule('wlan-ap'), 'Casa',, 0.8)
    #state['Casa'].out_actions.append(out_casa)
    #state['Default'].in_actions.append(default)
    while True:
        sleep(10)