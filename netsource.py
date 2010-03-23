#!/usr/bin/env python

import sys
sys.path.append("./cnetworkmanager.librarize")
from networkmanager.networkmanager import NetworkManager

nm = NetworkManager()

def getMacAddresses():
	return _getProperty('HwAddress')

def getSsids():
	return _getProperty('Ssid')

def _getProperty(property):
	devices = nm.GetDevices()
	result = []
	for dev in filter(lambda d: d._settings_type() == "802-11-wireless", devices):
		result.extend(str(ap[property]) for ap in dev.GetAccessPoints())
	return result
