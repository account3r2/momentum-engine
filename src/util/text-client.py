#!/usr/bin/env python3

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

# text-client.py : interface directly with the server via a terminal client

import sys
import socket
import json

com_sock = None

for res in socket.getaddrinfo(sys.argv[1], 12397, socket.AF_UNSPEC,
        socket.SOCK_DGRAM):
    fam, type, proto, cannonname, sockaddr = res

    try:
        com_sock = socket.socket(fam, type, proto)
    except OSError:
        com_sock = None
        continue

if com_sock is None:
    print("Could not get address")
    sys.exit(-1)

com_sock.settimeout(3)

while True:
    print("JSON packet to send:")
    packet_str = input("> ")

    com_sock.sendto(packet_str.encode(), (sys.argv[1], 12397))

    print("Waiting for server response...")

    try:
        data, host = com_sock.recvfrom(4096)
    except socket.timeout:
        print("Server did not respond within 3 seconds")
        continue

    print("Response packet :")
    print(json.dumps(json.loads(data.decode()), indent=4), "\n")
