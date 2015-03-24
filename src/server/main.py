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

# System imports
import socket
import json

# Project imports
import network
import player

connected_list = {}

while True:
    data, host = network.recv_packet()

    print("\nPacket recieved from", host[0])
    print("Packet is", len(data), "bytes long, contains", repr(data.decode()))

    try:
        json_packet = json.loads(data.decode())
    except ValueError:
        print("Packet is not valid JSON")
        continue

    print("Packet type is", repr(json_packet["type"]))

    if json_packet["type"] == "join":
        if not host[0] in connected_list:
            connected_list[host[0]] = player.Player(375, 275, 25, 25)
            network.send_packet(host, "success")
            print("Added host", host[0], "to connection list")
        else:
            network.send_packet(host, "failure", "Already connected")
            print("Host", host[0], "is already connected")

    if not host[0] in connected_list:
        print("Recieved packet from unknown host", host[0],". Ignoring.")
        continue

    if json_packet["type"] == "leave":
        del connected_list[host[0]]
        network.send_packet(host, "success")
        print("Host", host[0], "removed from connection list")
