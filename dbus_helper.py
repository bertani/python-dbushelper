#!/usr/bin/env python

 #####################################################################
#                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#                    Version 2, December 2004                         #
#                                                                     #
# Copyright (C) 2010 Thomas Bertani <sylar@anche.no>                  #
#                                                                     #
# Everyone is permitted to copy and distribute verbatim or modified   #
# copies of this license document, and changing it is allowed as long #
# as the name is changed.                                             #
#                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION   #
#                                                                     #
#  0. You just DO WHAT THE FUCK YOU WANT TO.                          #
#                                                                     #
 #####################################################################
#                                                                     #
#     DO WHAT YOU WANT CAUSE A PIRATE IS FREE, YOU ARE A PIRATE!      #
#                                                                     #
 #####################################################################

from dbus import SystemBus, Array
import xml.etree.ElementTree as et
from new import instancemethod

class Helper:
    __utils__ = {}
    def __init__(self, path):
        def addMethod(name, args=()):
            def f(x, *args):
                try:
                    return x.__utils__['obj'].get_dbus_method(name, path)(*args)
                except TypeError: raise Exception("Wrong arguments passed..")
            f.func_name = name
            f.func_doc = "Usage: %s(%s)" % (f.func_name, ','.join(args))
            setattr(self, name, instancemethod(f, self, self.__class__))
        self.__utils__['bus'] = SystemBus()
        if not path in self.__utils__['bus'].list_names():
            raise Exception("Cannot load path '%s'" % path)
        self.__utils__['obj'] = self.__utils__['bus'].get_object(path, "/")
        try: xml = et.fromstring(self.__utils__['obj'].Introspect())
        except: raise Exception("Introspection error")
        res = None
        for interface in xml.findall("interface"):
            while not res: res = interface if interface.get("name") == path else None
        for children in res._children:
            method_name = ""
            args = []
            method_name = children.get("name")
            for c in children._children:
                if (c.tag == "arg") and (c.get("direction") == "in"): args.append(c.get("name"))
            addMethod(method_name, args)
