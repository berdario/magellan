from time import sleep
from threading import Thread
import sys
import dbus

class NetworkSource():
    '''This class spawn a thread and fetch changes to the network using the NetworkManager DBUS API, calling the handlers provided when needed'''

    def __init__(self):
        

        self.bus=dbus.SystemBus()

        nm = dbus.Interface(self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"), "org.freedesktop.NetworkManager")
        devices= nm.GetDevices()
        self._wlan = []
        for d in devices:
            device=self.bus.get_object('org.freedesktop.NetworkManager',d)
            device_properties=dbus.Interface(device,"org.freedesktop.DBus.Properties")
            if device_properties.Get('org.freedesktop.DBus.Properties',"DeviceType") == 2:
                self._wlan.append(device)

        self.handlers = []
        self.p=Thread(target=self.run)
        self.p.daemon = True #simple solution, but it's better to be careful: http://joeshaw.org/2009/02/24/605
        self.p.start()
        
    def get_ssids(self):
        access_points=[]
        result=[]
        
        for w in self._wlan:
            wireless=dbus.Interface(w,'org.freedesktop.NetworkManager.Device.Wireless')
            access_points.extend(wireless.GetAccessPoints())
            
        for ap in access_points:
            ap_properties=dbus.Interface(self.bus.get_object('org.freedesktop.NetworkManager',ap),"org.freedesktop.DBus.Properties")
            ssid=ap_properties.Get('org.freedesktop.DBus.Properties',"Ssid")
            #for ssid in ssids:
            result.append(''.join((str(b) for b in ssid)))
                
        return result

    def connect_ssid(self, handler):
        '''Adds the handler to the functions to be called when an event happens or a change is detected'''
        self.handlers.append(handler)

    def run(self):
        while True:
            ssids = self.get_ssids()
            for f in self.handlers:
                f(ssids)
            sleep(2)

