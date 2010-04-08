#!/usr/bin/env python

import dbus
import xml.etree.ElementTree as et
from new import instancemethod
from exceptions import Exception

class Helper:
    __utils__ = {}
    def __init__(self, path):
        def addMethod(name):
            setattr(self, name, instancemethod(lambda x: x.__utils__['obj'].get_dbus_method(name).__call__(), self, self.__class__))
        self.__utils__['bus'] = dbus.SystemBus()
        if not path in self.__utils__['bus'].list_names():
            raise Exception("Cannot load path '%s'" % path)
        self.__utils__['obj'] = self.__utils__['bus'].get_object(path, "/")
        xml = et.fromstring(self.__utils__['obj'].Introspect())
        res = None
        for interface in xml.findall("interface"):
            for name, value in interface.items():
                if name == "name" and value == path: res = interface
            if res: break
        for children in res._children:
            _name = ""
            for name, value in children.items():
                if name == "name": _name = value
            addMethod(_name)

if __name__ == "__main__":
    a = Helper("org.neophysis.nde")
    print dir(a)
