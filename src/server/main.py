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
import sys
import json

# Add project top-level directory to import path
sys.path.append("..")

# Project imports
import common.network
import player

world = {
    "bounds" : (800, 600),
    "player" : {"host":""},
}

common.network.init_server()

while True:
    # Handle incoming packets
    json_packet, host = common.network.recv_packet()

    print("\nPacket recieved from", host[0])

    if json_packet is None:
        print("Packet is not valid JSON")
        continue

    if not "type" in json_packet:
        print("Packet has no 'type' object. Ignoring...")
        continue

    print("Packet type is", repr(json_packet["type"]))

    if json_packet["type"] == "join":
        if world["player"]["host"] == "":
            world["player"]["host"] = host[0]
            world["player"]["object"] = player.Player(375, 275, 25, 25)
            common.network.send_packet(host, "success")
            print("Added host", host[0], "to connection list")
        elif world["player"]["host"] == host[0]:
            common.network.send_packet(host, "failure",
                msg = "Already connected")
            print("Host", host[0], "is already connected")
        else:
            common.network.send_packet(host, "failure", msg = "Limit reached")

    if host[0] != world["player"]["host"]:
        print("Recieved packet from unknown host", host[0],". Ignoring.")
        continue

    if json_packet["type"] == "leave":
        world["player"]["host"] = ""
        del world["player"]["object"]
        common.network.send_packet(host, "success")
        print("Host", host[0], "disconnected")

    if json_packet["type"] == "retrieve":
        if not "what" in json_packet:
            common.network.send_packet(host, "failure",
                msg = "No object specified")
            continue

        if not json_packet["what"] in world:
            common.network.send_packet(host, "failure",
                msg = "No such value '{}'".format(json_packet["what"]))
            continue
        # Do a temporary special case check for Player class objects
        if json_packet["what"] == "player":
            common.network.send_packet(host, "retrieve",
                value = json.dumps(world["player"]["object"].__dict__,
                separators = (',',':')), what = json_packet["what"])
        else:
            common.network.send_packet(host, "retrieve",
                value = json.dumps(world[json_packet["what"]],
                separators = (',',':')), what = json_packet["what"])

    if json_packet["type"] == "update":
        # Assume we are updating the host's player

        if not "value" in json_packet:
            print("No value given in 'update' packet")
            continue

        for k in json_packet["value"]:
            world["player"]["object"][k] = json_packet["value"][k]
