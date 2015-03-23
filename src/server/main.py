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

import socket
import json

# Force IPv4 connections at the moment
# TODO: Make server IP version agnostic

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_sock.bind(("localhost", 12397))

while True:
    data, host = server_sock.recvfrom(4096)

    print("\nPacket recieved from", host[0])
    print("Packet is", len(data), "bytes long, contains", repr(data.decode()))

    try:
        json_packet = json.loads(data.decode())
    except ValueError:
        print("Packet is not valid JSON")
        continue

    print("Packet type is", json_packet["type"])
