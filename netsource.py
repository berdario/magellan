from time import sleep
from threading import Thread
import sys

sys.path.append("./cnetworkmanager.librarize")
from networkmanager.networkmanager import NetworkManager

class Network():
	"This class spawn a thread and fetch changes to the network using the NetworkManager DBUS API, calling the handlers provided when needed"

	def __init__(self):
		self.nm = NetworkManager()
		self.handlers = []
		self.p=Thread(target=self.run)
		self.p.daemon = True #simple solution, but it's better to be careful: http://joeshaw.org/2009/02/24/605
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
		"Adds the handler to the functions to be called when an event happens or a change is detected"
		self.handlers.append(handler)

	def run(self):
		while True:
			ssids = self.get_ssids()
			for f in self.handlers:		
				f(ssids)
			sleep(2)


