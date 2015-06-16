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

class Player():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xvel = 0
        self.yvel = 0
        self.xmovement = 0
        self.ymovement = 0
        self.in_air = True
        self.jump_vel = 25
        self.accel = 1 / 2

    def __getitem__(self, k):
        return self.__getattr__(k)

    def __setitem__(self, k, v):
        self.__setattr__(k, v)

    def update(self, bounds):
        self.x += int(self.xvel)
        self.y += int(self.yvel)

        if self.xmovement != 0:
            self.xvel += self.xmovement * self.accel
        else:
            if self.xvel > 0:
                self.xvel -= self.accel
            else:
                self.xvel += self.accel

        if self.ymovement == -1 and not self.in_air:
            self.in_air = True
            self.yvel -= self.jump_vel * self.accel
        else:
            self.yvel += self.accel

        if self.y < 0:
            self.yvel = -self.yvel
            self.y = 0

        if self.x < 0:
            self.xmovement = 0
            self.xvel = 0
            self.x = 0

        if self.y + self.h > bounds[1]:
            self.in_air = False
            self.yvel = 0
            self.y = bounds[1] - self.h

        if self.x + self.w > bounds[0]:
            self.xmovement = 0
            self.xvel = 0
            self.x = bounds[0] - self.w
