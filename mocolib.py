"""
Mocospace bot lib for python.

supports: multiple rooms, send chat message, recieve chat message, ignore, unignore, report, set color

All I ask is, if you give me credit for the lib.
NOTE: if you want to help develop this, please make a pull request.
"""


import ast
import json
import sys
import time as ut
import config
from threading import Thread as th
if sys.version_info[0] < 3:

    class urllib:
        parse = __import__("urllib")
        request = __import__("urllib2")
else:
    import urllib.request
    import urllib.parse


def make(part):
    return "http://www.mocospace.com" + part


class MocospaceApiServiceException(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class User(object):
    def __init__(self, **kw):
        self.name = None
        self.uid = None
        self.info = None

        for key, val in kw.items():
            if val == None:
                continue
            setattr(self, key, val)

    def __repr__(self):
        return "<user {0} obj_ref{1)>".format(self.user, id(self))


class Message(object):
    def __init__(self, **kw):
        self.name = None
        self.body = None
        self.color = None
        self.type = None
        self.time = None

        for key, val in kw.items():
            if val == None:
                continue
            setattr(self, key, val)

    def __repr__(self):
        return "<message.user={0}, message.body={1}, message.color={2}, message.type={3}, message.time={4}>".format(
            self.name, self.body, self.color, self.type, self.time)


class Mocospace(th):
    def __init__(self, room=None, mgr=None):
        self._room = room
        self._mgr = mgr
        self._msg = list()
        self._tc = list()
        th.__init__(self)

    def disconnect(self):
        self._disconnect()

    def message(self, msg):
        rid = self._make_id()
        now = ut.time() * 1000
        post = {
            "message": msg,
            "roomid": rid,
            "minTimestamp": now
        }
        data = urllib.parse.urlencode(post)
        req = urllib.request.Request(
            make(config.MOCO_SEND_MESSAGE), data, headers=config.MOCO_HEADERS)
        urllib.request.urlopen(req).read()

    def _make_id(self):
        # will be a url request soon
        f = open("room.ids", "r")
        roomids = ast.literal_eval(f.read())
        f.close()
        return roomids[self._room]

    def _make_connection(self):
        req = urllib.request.Request(make(config.MOCO_GET_MESSAGES.replace(
            "$ID", self._make_id())), headers=config.MOCO_HEADERS)
        resp = urllib.request.urlopen(req).read()
        return resp

    def _callEvent(self, evt, *args, **kw):
        if hasattr(self._mgr, evt):
            getattr(self._mgr, evt)(*args, **kw)

    def _disconnect(self):
        self._callEvent("0onDisconnect", self)
        sys.exit()

    def _connect(self):
        connection = self._make_connection()
        self._callEvent("onPing", self)
        return connection

    def _eventHandler(self, event):
        msgtype = int(event['messageType'])

        if msgtype == 0:
            userInfo = event['user']
            name = userInfo['name']
            body = event['message']
            try: color = event['color']
            except: color = "000000"
            timestamp = event['timestamp']
            uid=self.getUserId(name)
            user = User(name=name, uid=uid, info=userInfo)
            msg = Message(body=body, color=color, type=msgtype, time=timestamp)
            if len(self._msg) != 0:
                if msg.time not in self._tc:
                    self._tc = list()
                    self._tc.append(msg.time)
                    self._callEvent('onMessage', self , user, msg)
            else:
                if len(self._msg) == 0:
                    self._msg.append(msg)

        elif msgtype == 1:
            name = event['user']['name']
            uid=self.getUserId(name)
            timestamp = event['timestamp']
            msg = event['message']
            userInfo = event['user']
            user = User(name=name, uid=uid, info=userInfo)
            if len(self._msg) != 0 or timestamp in self._tc:
                self._tc = list()
                self._tc.append(timestamp)
                self._callEvent('onEnter', self, user)
            else:
                if len(self._msg) == 0:
                    self._msg.append(msg)

    def getUserId(self, name):
        req = urllib.request.Request(make(config.MOCO_USERS_IN_ROOM.replace("$ID", self._make_id())), headers=config.MOCO_HEADERS)
        response = urllib.request.urlopen(req).read().decode()
        response = json.loads(response)
        event = response['ApiSearchResult'][0]['searchResults']
        while True:
            for data in event:
                if data['name'] == name:
                    return data['uid']
            return None

    def startThread(self):
        self.start()

    def run(self):
        while True:
            events = self._connect()
            response = json.loads(events)
            try:
                event = response['ChatEntry'][0]
                self._eventHandler(event)
                ut.sleep(self._mgr.timer)
            except:
                raise MocospaceApiServiceException(event['ApiServiceException'][0]['message'])

    def getRoomName(self): return self._room

    def getRoomId(self): return self._make_id()

    def getRoomNames(self): return self._mgr.getRoomNames()

    name = property(getRoomName)
    id = property(getRoomId)
    roomnames = property(getRoomNames)

class RoomManager(object):
    _rooms = list()
    def __init__(self):
        self.timer = 3
        self.onInit()

    def joinRoom(self, room):
        room = Mocospace(room, self)
        self._rooms.append(room)
        return room

    def leaveRoom(self, room):
        for r in self._rooms:
            if r.name == room:
                room.disconnect()
                self._rooms.remove(r)

    def run(self):
        for room in self._rooms:
            self._startThread(room)

    def onPing(self, room):
        pass

    def onDisconnect(self, room):
        pass

    def onMessage(self, room, user, msg):
        pass

    def onInit(self):
        pass

    def ignoreUser(self, uid):
        '''
        ignore a user

        @uid: User id of the user you want ignored
        '''

        post = {"userid": uid}
        data = urllib.parse.urlencode(post)
        req = urllib.request.Request(
            make(config.MOCO_IGNORE_USER), data, headers=config.MOCO_HEADERS)
        urllib.request.urlopen(req).read().decode()

    def unignoreUser(self, uid):
        '''
        stop ignoring the user

        @uid: User id of the ignored person
        '''

        post = {"userid": uid}
        data = urllib.parse.urlencode(post)
        req = urllib.request.Request(
            make(config.MOCO_UNIGNORE_USER), data, headers=config.MOCO_HEADERS)
        urllib.request.urlopen(req).read().decode()

    def setColor(self, color):
        '''
        change font color

        @color: The color of the message (html hex colors)
        '''

        color = color.replace("#", "")
        post = {"color": color}
        data = urllib.parse.urlencode(post)
        req = urllib.request.Request(
            make(config.MOCO_SET_COLOR), data, headers=config.MOCO_HEADERS)
        urllib.request.urlopen(req).read().decode()

    def reportUser(self, uid, comment):
        '''
        report a user

        @uid: User id of the user
        @comment: The message to be sent to mocospace
        '''
        post = {
            'userid': uid,
            'comment': comment
        }
        data = urllib.parse.urlencode(post)
        req = urllib.request.Request(
            make(config.MOCO_REPORT_USER), data, headers=config.MOCO_HEADERS)
        urllib.request.urlopen(req).read().decode()

    def _startThread(self, room):
        room.startThread()

    def getRooms(self): return self._rooms

    def getRoomNames(self): return [room.name for room in self._rooms]

    roomnames = property(getRoomNames)
