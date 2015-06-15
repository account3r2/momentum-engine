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

class Player():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xmovement = 0
        self.ymovement = 0

    def __getitem__(self, k):
        getattr(self, k)

    def __setitem__(self, k, v):
        self.__setattr__(k, v)

    def render(self, context):
        player_rect = SDL_Rect(x = self.x, y = self.y, w = self.w, h = self.h)
        SDL_SetRenderDrawColor(context, 0xff, 0xff, 0xff, 0)
        SDL_RenderFillRect(context, ctypes.byref(player_rect))
        SDL_SetRenderDrawColor(context, 0, 0, 0, 0)
