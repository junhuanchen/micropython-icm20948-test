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
from machine import I2C, Pin

""" ---------------------------------------------------------------------- """
# for singleton pattern
# Implement used global value,
# maybe Micropython 'function' object can't have attribute...
__i2c = None


def get_i2c_object():
    global __i2c
    if __i2c is None:
        __i2c = I2C(scl=Pin(22), sda=Pin(21))
    return __i2c

""" ---------------------------------------------------------------------- """
""" I2C bus -------------------------------------------------------------- """


class StuduinoBitI2C:
    """I2C is not emulated.
    """
    def __init__(self):
        self._i2c = get_i2c_object()

    def init(self, freq=100000, scl=Pin(22), sda=Pin(21)):
        self._i2c.init(freq=freq, scl=scl, sda=sda)

    def scan(self):
        return self._i2c.scan()

    def read(self, addr, n, repeat=False):
        return self._i2c.readfrom(addr, n)

    def write(self, addr, buf, repeat=False):
        """Not implemented """
        pass

""" ---------------------------------------------------------------------- """
""" SPI bus -------------------------------------------------------------- """


class StuduinoBitSPI:
    def __init__(self):
        """Not implemented """
        pass

    def init(baudrate=1000000, bits=8, mode=0, sclk=0, mosi=0, miso=0):
        raise NotImplementedError

    def read(self, nbytes):
        raise NotImplementedError

    def write(self, buffer):
        raise NotImplementedError

    def write_readinto(self, out, inbuf):
        raise NotImplementedError
