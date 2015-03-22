# System imports
import ctypes
from sdl2 import *

class Player():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xvel = 0
        self.yvel = 0

    def update(self, bounds):
        self.x += int(self.xvel)
        self.y += int(self.yvel)

        if self.y < 0:
            self.yvel = 0
            self.y = 0

        if self.x < 0:
            self.xvel = 0
            self.x = 0

        if self.y + self.h > bounds[1]:
            self.yvel = 0
            self.y = bounds[1] - self.h

        if self.x + self.w > bounds[0]:
            self.xvel = 0
            self.x = bounds[0] - self.w

    def render(self, context):
        sdl_rect = SDL_Rect(x = self.x, y = self.y, w = self.w, h = self.h)
        SDL_FillRect(context, ctypes.byref(sdl_rect), ctypes.c_uint(0x00ffffff))
