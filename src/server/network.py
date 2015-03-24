# Momentum Engine - 2D Semi-real Physics Platforming Engine
#
# Copyright (C) 2015 Robert Cochran
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License in the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import socket
import json

# Ugly hack to make sure that __server_sock is actually
# a socket, otherwise Python will throw up on it

# Force IPv4 connections at the moment
# TODO: Make server IP version agnostic

__server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
__server_sock.bind(("localhost", 12397))

def recv_packet():
    return __server_sock.recvfrom(4096)

def send_packet(host, msg_type, msg = ''):
    packet = json.dumps(dict(type = msg_type, msg = msg),
            separators = (',',':'))
    __server_sock.sendto(packet.encode(), host)
