"""
------------------------------------------------------------------------------
The MIT License (MIT)
Copyright (c) 2016 Newcastle University
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.import time
------------------------------------------------------------------------------
Author
Kenji Kawase, Artec Co., Ltd.
------------------------------------------------------------------------------
"""
import ustruct
from micropython import const


class ICMRegisterRW:
    def __init__(self, i2c, address):
        self._i2c = i2c
        self._address = address

    def register_short(self, register, value=None,
                       buf=bytearray(2), endian='b'):
        if endian is 'b':
            fmt = ">h"
        else:
            fmt = "<h"

        if value is None:
            self._i2c.readfrom_mem_into(self._address, register, buf)
            return ustruct.unpack(fmt, buf)[0]

        ustruct.pack_into(fmt, buf, 0, value)
        return self._i2c.writeto_mem(self._address, register, buf)

    def register_three_shorts(self, register, buf=bytearray(6), endian='b'):
        if endian is 'b':
            fmt = ">hhh"
        else:
            fmt = "<hhh"

        self._i2c.readfrom_mem_into(self._address, register, buf)
        return ustruct.unpack(fmt, buf)

    def register_char(self, register, value=None, buf=bytearray(1)):
        if value is None:
            self._i2c.readfrom_mem_into(self._address, register, buf)
            return buf[0]

        ustruct.pack_into("<b", buf, 0, value)
        return self._i2c.writeto_mem(self._address, register, buf)
