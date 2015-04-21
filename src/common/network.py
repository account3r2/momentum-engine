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

def init_server():
    # TODO: IP is always v4. Make it agnostic.
    global __sock__
    __sock__ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    __sock__.bind((socket.gethostname(), 12397))

def init_client(addr, port):
    global __sock__
    for r in socket.getaddrinfo(addr, port, socket.AF_UNSPEC,
            socket.SOCK_DGRAM):
        fam, type, proto, cannonname, sockaddr = r

        try:
            __sock__ = socket.socket(fam, type, proto)
        except OSError:
            __sock__ = None
            continue

    return __sock__ is not None

def recv_packet():
    global __sock__
    data, host = __sock__.recvfrom(4096)

    try:
        packet = json.loads(data.decode())
    except ValueError:
        return None, host

    return packet, host

def send_packet(host, msg_type, **params):
    global __sock__
    packet = json.dumps(dict(type = msg_type, **params),
        separators = (',',':'))
    __sock__.sendto(packet.encode(), host)
