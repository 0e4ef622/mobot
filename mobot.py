#!/usr/bin/env python3

import time
import dbus
from gi.repository import GObject
from dbus.decorators import method
import dbus.mainloop.glib
import dbus.service

import re
import subprocess

#chatid = "#abemaster446/$9c20ed649fd06f85" # (bot testing chat thing)

def skype_event(eventstr):
    split = re.split(r'\s', eventstr)
    evtype = split[0]
    if split[0] == "CHATMESSAGE" and (split[3] == "RECEIVED" or split[3] == "SENDING"):

        msgid = split[1]
        dispname = re.search("^CHATMESSAGE %s FROM_DISPNAME (.*)$" % msgid, send("GET CHATMESSAGE %s FROM_DISPNAME" % msgid)).group(0)
        msg = re.match("^CHATMESSAGE %s BODY (.*)$" % msgid, send("GET CHATMESSAGE %s BODY" % msgid)).group(1)
        chatid = re.search("[^\s]+$", send("GET CHATMESSAGE %s CHATNAME" % msgid)).group(0)

        #if re.search(r'uotd\?$', msg, re.I): # temporary before learndb is created
        #    send("CHATMESSAGE %s %s: UOTD: Uzzol Of The Day" % (chatid, dispname))

        if msg == 'hai':
            send("CHATMESSAGE %s hai %s" % (chatid, dispname))
        elif re.match('!ping', msg):
            send("CHATMESSAGE %s %s: yes i exist" % (chatid, dispname))
        elif re.match('!fortune', msg):
            send("CHATMESSAGE %s %s: %s" % (chatid, dispname, str(subprocess.check_output("fortune"), encoding='utf-8')))


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

ret = send("NAME ijs")
if ret != "OK":
    raise Exception("Y U NO LEMME DO MY SHET")

ret = send("PROTOCOL 7")
if ret != "PROTOCOL 7":
    raise Exception("Y U NO MATCH PROTOCOLS???")

hai = skype_notify(bus)

mainloop = GObject.MainLoop()
mainloop.run()
