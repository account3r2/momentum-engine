#!/usr/bin/env python3

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
            if event.key.keysym.scancode == SDL_SCANCODE_W:
                keyboard_ycontrol -= 1

            elif event.key.keysym.scancode == SDL_SCANCODE_S:
                keyboard_ycontrol += 1

            elif event.key.keysym.scancode == SDL_SCANCODE_A:
                keyboard_xcontrol -= 1

            elif event.key.keysym.scancode == SDL_SCANCODE_D:
                keyboard_xcontrol += 1

        elif event.type == SDL_KEYUP:
            if event.key.keysym.scancode == SDL_SCANCODE_W:
                keyboard_ycontrol += 1

            elif event.key.keysym.scancode == SDL_SCANCODE_S:
                keyboard_ycontrol -= 1

            elif event.key.keysym.scancode == SDL_SCANCODE_A:
                keyboard_xcontrol += 1

            elif event.key.keysym.scancode == SDL_SCANCODE_D:
                keyboard_xcontrol -= 1

    # Logic
    my_player.yvel += keyboard_ycontrol * player_accel_factor
    my_player.xvel += keyboard_xcontrol * player_accel_factor

    my_player.update(win_size)

    # Render

    # Clear screen
    SDL_FillRect(window_surf, None, ctypes.c_uint(0))

    my_player.render(window_surf)

    SDL_UpdateWindowSurface(window)

SDL_DestroyWindow(window)
SDL_Quit()
