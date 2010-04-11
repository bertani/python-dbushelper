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

from dbus import SystemBus
from xml.etree.ElementTree import fromstring
from new import instancemethod

class Helper:
    '''
    This helper lets you simply call dbus methods as if they are provided by this class.
    The usage is Helper(path), so you have just to call the constructor with the complete path (or a part of it if it's unique) of the dbus interface whose methods you are interested in.
    
    Example: Helper("org.neophysis.nwm") or just Helper("nwm")
    '''
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
        r = []
        for i in self.__utils__['bus'].list_names():
            r.append(i) if (i.find(path) > -1) else None
        if not len(r): raise Exception("Cannot find any matching interface as '%s'" % path)
        elif len(r) == 1: path = r[0]
        else: raise Exception("The path specified is ambiguos: %s maching interfaces found" % len(r))
        self.__utils__['obj'] = self.__utils__['bus'].get_object(path, "/")
        try: xml = fromstring(self.__utils__['obj'].Introspect())
        except: raise Exception("Introspection error")
        res = None
        for interface in xml.findall("interface"):
            while not res: res = interface if interface.get("name") == path else None
        for children in res._children:
            args = []
            method_name = children.get("name")
            for c in children._children:
                if (c.tag == "arg") and (c.get("direction") == "in"): args.append(c.get("name"))
            addMethod(method_name, args)
