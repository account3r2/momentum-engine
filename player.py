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

    def update(self):
        self.x += self.xvel
        self.y += self.yvel

    def render(self, context):
        sdl_rect = SDL_Rect(x = self.x, y = self.y, w = self.w, h = self.h)
        SDL_FillRect(context, ctypes.byref(sdl_rect), ctypes.c_uint(0x00ffffff))
