#!/usr/bin/env python3

import time
import dbus
from gi.repository import GObject
from dbus.decorators import method
import dbus.mainloop.glib
import dbus.service

import re
import subprocess
import cmds

#chatid = "#abemaster446/$9c20ed649fd06f85" # (bot testing chat thing)

def chat(chatid, msg):
    send("CHATMESSAGE %s %s" % (chatid, msg))

def skype_event(eventstr):
    split = re.split(r'\s', eventstr)
    evtype = split[0]
    if split[0] == "CHATMESSAGE" and (split[3] == "RECEIVED" or split[3] == "SENDING"):

        msgid = split[1]
        dispname = re.search("^CHATMESSAGE %s FROM_DISPNAME (.*)$" % msgid, send("GET CHATMESSAGE %s FROM_DISPNAME" % msgid)).group(1)
        msg = re.match("^CHATMESSAGE %s BODY (.*)$" % msgid, send("GET CHATMESSAGE %s BODY" % msgid), re.S).group(1)
        chatid = re.search("[^\s]+$", send("GET CHATMESSAGE %s CHATNAME" % msgid)).group(0)

        if msg.lower() == 'hai' or msg.lower() == 'hi':
            chat(chatid, 'hai %s' % dispname)
        elif msg[0:4] == 'Ni!':
            chat(chatid, '%s: Do you demand a shrubbery?' % dispname)

        else:
            m = re.match(r'^([^\s]+)\s*(.*)$', msg, re.S)

            if m:
                cmd = m.group(1).lower()
                argstr = m.group(2)
                if cmd in cmds.cmds:
                    cmds.cmds[cmd](chat, chatid, dispname, argstr)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
skype = bus.get_object("com.Skype.API", "/com/Skype")

class skype_notify(dbus.service.Object):
    def __init__(self, bus):
        dbus.service.Object.__init__(self, bus, "/com/Skype/Client")

    @method(dbus_interface="com.Skype.API.Client", in_signature="s")
    def Notify(self, s=None):
        if s:
            print("notify <- "+s)
            skype_event(s)

def send(msg):
    print("-> ", msg)
    ret = skype.Invoke(msg);
    print("<- ", ret)
    return ret

ret = send("NAME mobot")
if ret != "OK":
    raise Exception("Y U NO LEMME DO MY SHET")

ret = send("PROTOCOL 7")
if ret != "PROTOCOL 7":
    raise Exception("Y U NO MATCH PROTOCOLS???")

hai = skype_notify(bus)

mainloop = GObject.MainLoop()
mainloop.run()
