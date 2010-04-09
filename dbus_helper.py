#!/usr/bin/env python

from dbus import SystemBus, Array
import xml.etree.ElementTree as et
from new import instancemethod

class Helper:
    __utils__ = {}
    def __init__(self, path):
        def addMethod(name, signature="sv", args=()):
            def f(x, *args):
                try:
                    res = x.__utils__['obj'].get_dbus_method(name, path)(*args)
                    return res
                except TypeError: return "Wrong arguments passed.."
            f.func_name = name
            doc = "Usage: %s(" % f.func_name
            for arg in args: doc += "%s," % arg
            doc = doc[:-1] + ")"
            f.func_doc = doc
            setattr(self, name, instancemethod(f, self, self.__class__))
        self.__utils__['bus'] = SystemBus()
        if not path in self.__utils__['bus'].list_names():
            print "Cannot load path '%s'" % path
            return
        self.__utils__['obj'] = self.__utils__['bus'].get_object(path, "/")
        xml = self.__utils__['obj'].Introspect()
        xml = et.fromstring(xml)
        res = None
        for interface in xml.findall("interface"):
            res = interface if interface.get("name") == path else None
            if res: break
        for children in res._children:
            method_name, signature = "", ""
            args = []
            method_name = children.get("name")
            for c in children._children:
                if c.tag == "arg":
                    if c.get("direction") == "in": args.append(c.get("name"))
                    else: signature = c.get("type")
            addMethod(method_name, signature, args)
