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
import ctypes
from sdl2 import *

# Add project top-level directory to import path
sys.path.append("..")

# Project imports
import common.network
import player
import fps

server_addr = "localhost" if len(sys.argv) < 2 else sys.argv[1]

if not common.network.init_client(server_addr, 12397):
    print("Could not connect to server!")
    sys.exit(-1)

server = (server_addr, 12397)

common.network.send_packet(server, "join")
resp, host = common.network.recv_packet()

if resp["type"] == "failure":
    print("Join failed:", resp["msg"])
    sys.exit(-1)
elif resp["type"] != "success":
    print("Got unexpected '{}' packet. Bailing out...".format(resp["type"]))
    sys.exit(-1)

common.network.send_packet(server, "retrieve", what = "bounds")
resp, host = common.network.recv_packet()

value = json.loads(resp["value"])

win_size = value[0], value[1]

common.network.send_packet(server, "retrieve", what = "player")
resp, host = common.network.recv_packet()

value = json.loads(resp["value"])

my_player = player.Player(value["x"], value["y"], value["w"], value["h"])

# List of keys that are down
keys_down = []

SDL_Init(SDL_INIT_VIDEO)

window = SDL_CreateWindow(b"Momentum Engine Client", SDL_WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_CENTERED, win_size[0], win_size[1], 0)
window_render = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

run = True
event = SDL_Event()

while run:
    frame_start = SDL_GetTicks()

    while SDL_PollEvent(ctypes.byref(event)):
        if event.type == SDL_QUIT:
            run = False
            break

        elif event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == SDLK_w and "w" not in keys_down:
                keys_down.append("w")
                common.network.send_packet(server, "update",
                    value = {"ymovement" : my_player.ymovement - 1})

            elif event.key.keysym.sym == SDLK_s and "s" not in keys_down:
                keys_down.append("s")
                common.network.send_packet(server, "update",
                    value = {"ymovement" : my_player.ymovement + 1})

            elif event.key.keysym.sym == SDLK_a and "a" not in keys_down:
                keys_down.append("a")
                common.network.send_packet(server, "update",
                    value = {"xmovement" : my_player.xmovement - 1})

            elif event.key.keysym.sym == SDLK_d and "d" not in keys_down:
                keys_down.append("d")
                common.network.send_packet(server, "update",
                    value = {"xmovement" : my_player.xmovement + 1})

        elif event.type == SDL_KEYUP:
            if event.key.keysym.sym == SDLK_w and "w" in keys_down:
                keys_down.remove("w")
                if my_player.ymovement == 0: continue

                common.network.send_packet(server, "update",
                    value = {"ymovement" : my_player.ymovement + 1})

            elif event.key.keysym.sym == SDLK_s and "s" in keys_down:
                keys_down.remove("s")
                if my_player.ymovement == 0: continue

                common.network.send_packet(server, "update",
                    value = {"ymovement" : my_player.ymovement - 1})

            elif event.key.keysym.sym == SDLK_a and "a" in keys_down:
                keys_down.remove("a")
                if my_player.xmovement == 0: continue

                common.network.send_packet(server, "update",
                    value = {"xmovement" : my_player.xmovement + 1})

            elif event.key.keysym.sym == SDLK_d and "d" in keys_down:
                keys_down.remove("d")
                if my_player.xmovement == 0: continue

                common.network.send_packet(server, "update",
                    value = {"xmovement" : my_player.xmovement - 1})

    common.network.send_packet(server, "retrieve", what = "player")
    packet, host = common.network.recv_packet()

    value = json.loads(packet["value"])

    for k in value:
        my_player[k] = value[k]

    # Render

    SDL_RenderClear(window_render)

    my_player.render(window_render)

    SDL_RenderPresent(window_render)

    # Sleep to maintain 60 FPS if necessary
    if int(1000 / 60) > (SDL_GetTicks() - frame_start):
        SDL_Delay(int(1000 / 60) - (SDL_GetTicks() - frame_start))

    # Record frame time
    fps.add_frame((SDL_GetTicks() - frame_start) / 1000)

common.network.send_packet(server, "leave")

SDL_DestroyWindow(window)
SDL_Quit()
