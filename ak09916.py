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
MicroPython I2C driver for AK09916 magnetometer
Author
Kenji Kawase, Artec Co., Ltd.
We used the script below as reference
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/master/MicroPython_BUILD/components/micropython/esp32/modules_examples/drivers/ak8963.py
------------------------------------------------------------------------------
"""
import utime
from machine import I2C, Pin
from micropython import const
from icm_register_rw import ICMRegisterRW

__version__ = "0.2.0"

_WIA = const(0x01)
_HXL = const(0x11)
_HXH = const(0x12)
_HYL = const(0x13)
_HYH = const(0x14)
_HZL = const(0x15)
_HZH = const(0x16)
_ST2 = const(0x18)
_CNTL2 = const(0x31)
_ASAX = const(0x60)
_ASAY = const(0x61)
_ASAZ = const(0x62)

_MODE_POWER_DOWN = 0b00000000
MODE_SINGLE_MEASURE = 0b00000001
MODE_CONTINOUS_MEASURE_1 = 0b00000010   # 10Hz
MODE_CONTINOUS_MEASURE_2 = 0b00001000   # 100Hz
MODE_EXTERNAL_TRIGGER_MEASURE = 0b00000100
_MODE_SELF_TEST = 0b00001000
_MODE_FUSE_ROM_ACCESS = 0b00011111

OUTPUT_14_BIT = 0b00000000
OUTPUT_16_BIT = 0b00010000

_SO_14BIT = 0.6     # per digit when 14bit mode
_SO_16BIT = 0.15    # per digit when 16bit mode


class AK09916(ICMRegisterRW):
    ADDR = 0x0c
    """Class which provides interface to AK09916 magnetometer."""
    def __init__(self, i2c):
        super().__init__(i2c, AK09916.ADDR)

        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)

        # if AK09916.ADDR != self.whoami:
        #    raise RuntimeError("AK09916 not found in I2C bus.")

        # Sensitivity adjustement values
        # self.register_char(_CNTL2, _MODE_FUSE_ROM_ACCESS)
        # asax = self.register_char(_ASAX)
        # asay = self.register_char(_ASAY)
        # asaz = self.register_char(_ASAZ)
        # self.register_char(_CNTL2, _MODE_POWER_DOWN)

        # Should wait atleast 100us before next mode
        # self._adjustement = (
        #     (0.5 * (asax - 128)) / 128 + 1,
        #     (0.5 * (asay - 128)) / 128 + 1,
        #     (0.5 * (asaz - 128)) / 128 + 1
        # )

        # Power on
        self.register_char(_CNTL2, MODE_CONTINOUS_MEASURE_1)

        self._so = _SO_16BIT

    @property
    def magnetic(self):
        """
        X, Y, Z axis micro-Tesla (uT) as floats.
        """
        # self.register_char(_CNTL2, MODE_SINGLE_MEASURE)
        # xyz = list(self.register_three_shorts(_HXL, endian='l'))
        x = self.register_short(_HXL, endian='l')
        y = self.register_short(_HYL, endian='l')
        z = self.register_short(_HZL, endian='l')
        xyz = [x, y, z]

        self.register_char(_ST2)    # Enable updating readings again

        # Apply factory axial sensitivy adjustements
        # xyz[0] *= self._adjustement[0]
        # xyz[1] *= self._adjustement[1]
        # xyz[2] *= self._adjustement[2]

        # Apply output scale determined in constructor
        so = self._so
        xyz[0] *= so
        xyz[1] *= so
        xyz[2] *= so

        # Apply hard iron ie. offset bias from calibration
        xyz[0] -= self._offset[0]
        xyz[1] -= self._offset[1]
        xyz[2] -= self._offset[2]

        # Apply soft iron ie. scale bias from calibration
        xyz[0] *= self._scale[0]
        xyz[1] *= self._scale[1]
        xyz[2] *= self._scale[2]

        # print('offset:{0}'.format(self._offset))
        # print('scale:{0}'.format(self._scale))

        return tuple(xyz)

    # @property
    # def adjustement(self):
    #     return self._adjustement

    @property
    def whoami(self):
        """ Value of the whoami register. """
        return self.register_char(_WIA)

    def calibrate(self, count=256, delay=200):
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)

        reading = self.magnetic
        minx = maxx = reading[0]
        miny = maxy = reading[1]
        minz = maxz = reading[2]

        while count:
            utime.sleep_ms(delay)
            reading = self.magnetic
            minx = min(minx, reading[0])
            maxx = max(maxx, reading[0])
            miny = min(miny, reading[1])
            maxy = max(maxy, reading[1])
            minz = min(minz, reading[2])
            maxz = max(maxz, reading[2])
            count -= 1

        # Hard iron correction
        offset_x = (maxx + minx) / 2
        offset_y = (maxy + miny) / 2
        offset_z = (maxz + minz) / 2

        self._offset = (offset_x, offset_y, offset_z)

        # Soft iron correction
        avg_delta_x = (maxx - minx) / 2
        avg_delta_y = (maxy - miny) / 2
        avg_delta_z = (maxz - minz) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

        scale_x = avg_delta / avg_delta_x
        scale_y = avg_delta / avg_delta_y
        scale_z = avg_delta / avg_delta_z

        self._scale = (scale_x, scale_y, scale_z)

        return self._offset, self._scale

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass
