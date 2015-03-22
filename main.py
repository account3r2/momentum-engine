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
import ctypes
from sdl2 import *

# Project imports
import player

my_player = player.Player(375, 275, 25, 25)
player_accel_factor = 1 / 8

SDL_Init(SDL_INIT_VIDEO)

win_size = (800, 600)

window = SDL_CreateWindow(b"Momentum Engine", SDL_WINDOWPOS_CENTERED,
                          SDL_WINDOWPOS_CENTERED, win_size[0],
                          win_size[1], 0)
window_surf = SDL_GetWindowSurface(window)

run = True
event = SDL_Event()

keyboard_xcontrol = 0
keyboard_ycontrol = 0

while run:
    while SDL_PollEvent(ctypes.byref(event)):
        if event.type == SDL_QUIT:
            run = False
            break

        elif event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == SDLK_w:
                keyboard_ycontrol -= 1

            elif event.key.keysym.sym == SDLK_s:
                keyboard_ycontrol += 1

            elif event.key.keysym.sym == SDLK_a:
                keyboard_xcontrol -= 1

            elif event.key.keysym.sym == SDLK_d:
                keyboard_xcontrol += 1

        elif event.type == SDL_KEYUP:
            if event.key.keysym.sym == SDLK_w:
                keyboard_ycontrol += 1

            elif event.key.keysym.sym == SDLK_s:
                keyboard_ycontrol -= 1

            elif event.key.keysym.sym == SDLK_a:
                keyboard_xcontrol += 1

            elif event.key.keysym.sym == SDLK_d:
                keyboard_xcontrol -= 1

    # Logic
    if keyboard_ycontrol != 0:
        my_player.yvel += keyboard_ycontrol * player_accel_factor
    else:
        if my_player.yvel > 0:
            my_player.yvel -= player_accel_factor
        else:
            my_player.yvel += player_accel_factor

    if keyboard_xcontrol != 0:
        my_player.xvel += keyboard_xcontrol * player_accel_factor
    else:
        if my_player.xvel > 0:
            my_player.xvel -= player_accel_factor
        else:
            my_player.xvel += player_accel_factor

    my_player.update(win_size)

    # Render

    # Clear screen
    SDL_FillRect(window_surf, None, ctypes.c_uint(0))

    my_player.render(window_surf)

    SDL_UpdateWindowSurface(window)

SDL_DestroyWindow(window)
SDL_Quit()
