from time import sleep
from threading import Thread
from functools import partial
import sys

sys.path.append("./cnetworkmanager.librarize")
from networkmanager.networkmanager import NetworkManager

class Network():
	def __init__(self):
		self.nm = NetworkManager()
		self.handlers = []
		self.p=Thread(target=self.run)
		self.p.start()
		
	def get_macaddresses(self):
		return self._getProperty('HwAddress')

	def get_ssids(self):
		return self._getProperty('Ssid')

	def _getProperty(self, property):
		devices = self.nm.GetDevices()
		result = []
		for dev in filter(lambda d: d._settings_type() == "802-11-wireless", devices):
			result.extend(str(ap[property]) for ap in dev.GetAccessPoints())
		return result

	def connect_ssid(self, handler):
		self.handlers.append(handler)

	def run(self):
		while True:
			ssids = self.get_ssids()
			for f in self.handlers:		
				f(ssids)
			sleep(2)

class SmartNetwork():
	def __init__(self):
		self.nm = NetworkManager()
		self.handlers = {}
		self.p=Thread(target=self.run)
		self.p.start()
		
	def get_macaddresses(self):
		return self._getProperty('HwAddress')

	def get_ssids(self):
		return self._getProperty('Ssid')

	def _getProperty(self, property):
		devices = self.nm.GetDevices()
		result = []
		for dev in filter(lambda d: d._settings_type() == "802-11-wireless", devices):
			result.extend(str(ap[property]) for ap in dev.GetAccessPoints())
		return result

	def connect_ssid(self, handler, value):
		self.handlers[handler] = value

	def run(self):
		while True:
			ssids = self.get_ssids()
			for f in self.handlers:	
				if self.handlers[f] in ssids:
					f()
			sleep(2)


	



#add_rule(network.connect_ssid,'unibgfreenet','in uni',0.8)

#partial(network.connect_ssid,)


#network.connect_ssid(university_rule)
#network.connect_ssid(home_rule)


