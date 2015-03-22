#!/usr/bin/env python3

# System imports
import ctypes
from sdl2 import *

# Project imports
import player

my_player = player.Player(375, 275, 25, 25)

SDL_Init(SDL_INIT_VIDEO)

window = SDL_CreateWindow(b"Momentum Engine", SDL_WINDOWPOS_CENTERED,
                               SDL_WINDOWPOS_CENTERED, 800, 600, 0)
window_surf = SDL_GetWindowSurface(window)

run = True
event = SDL_Event()

while run:
    while SDL_PollEvent(ctypes.byref(event)):
        if event.type == SDL_QUIT:
            run = False
            break

        elif event.type == SDL_KEYDOWN:
            pass

    # Clear screen
    SDL_FillRect(window_surf, None, ctypes.c_uint(0))

    my_player.update()

    my_player.render(window_surf)

    SDL_UpdateWindowSurface(window)

SDL_DestroyWindow(window)
SDL_Quit()
