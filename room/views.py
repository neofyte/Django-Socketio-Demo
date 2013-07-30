# Create your views here.
import os 

from gevent import monkey
monkey.patch_all(
    socket=True, dns=True, 
    time=True, select=True,
    thread=False, os=True, 
    ssl=True, httplib=False, 
    aggressive=True
    )

from gevent import Greenlet

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

def mainpage(request):
    """Render the meeting room page."""
    context = RequestContext(request)
    return render_to_response('room.html', {}, context)

def meeting_room(request,path):
    socketio_manage(request.environ, {'': MeetingRoomNamespace})

    return HttpResponse()

# The socket.io namespace
@namespace('/')
class MeetingRoomNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_nickname(self, nickname):
        self.environ.setdefault('nicknames', []).append(nickname)
        self.socket.session['nickname'] = nickname
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.environ['nicknames'])
        # Just have them join a default-named room
        self.join('main_room')

    def on_user_message(self, msg):
        self.emit_to_room('main_room', 'msg_to_room', self.socket.session['nickname'], msg)

    def recv_message(self, message):
        print ("PING!!!", message)

