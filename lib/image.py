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
We used the script below as reference
https://github.com/casnortheast/microbit_stub/
------------------------------------------------------------------------------
"""
import array
from .common import _rgb_24bit, _24bit_rgb
from .const import *

""" ---------------------------------------------------------------------- """
""" Images --------------------------------------------------------------- """


class StuduinoBitImage(BuiltinColor):
    """Represents an image that can be displayed on the microbit screen.
    """
    __SEP = ':'
    __WIDTH_DEFAULT = 5
    __HEIGHT_DEFAULT = 5
    __PAD = 0
    __PIX_MIN = 0
    __PIX_MAX = 9
    __PIX_MAXCOLOR_FACTOR = 0x1f
    __PIX_MAXCOLOR = 0xffffff

    def __fromsize(args):
        width = args[0]
        height = args[1]

        if width < 0 or height < 0:
            raise ValueError('image is incorrect size')

        return [[StuduinoBitImage.__PIX_MIN for x in range(width)]
                for y in range(height)]

    def __default(args):
        return StuduinoBitImage.__fromsize([StuduinoBitImage.__WIDTH_DEFAULT,
                                            StuduinoBitImage.__HEIGHT_DEFAULT])

    def __fromstring(args):
        s = args[0]
        if type(s) is not str:
            raise TypeError('Image(s) takes a string')

        if not s:
            return []

        t = s.replace(':', '')

        if not t:
            return StuduinoBitImage.__default(args)

        if not t.isdigit():
            raise ValueError('Unexpected character in Image definition')

        rows = s.rstrip(StuduinoBitImage.__SEP).split(StuduinoBitImage.__SEP)
        width = max([len(r) for r in rows])

        arr = []
        for r in rows:
            temp = []
            if len(r) == width:
                for char in r:
                    if (int(char) > 0):
                        temp.append(1)
                    else:
                        temp.append(0)
            else:
                for char in r:
                    if (int(char) > 0):
                        temp.append(1)
                    else:
                        temp.append(0)
                for i in range(width - len(r)):
                    temp.append(StuduinoBitImage.__PAD)
            arr.append(temp)

        return arr

    def __frombuffer(args):
        width = args[0]
        height = args[1]
        buffer = args[2]

        if buffer is None or type(buffer) is not array.array:
            raise TypeError('(array) object with buffer protocol required')

        if len(buffer) != width*height:
            raise ValueError('image data is incorrect size')

        if not buffer:
            return []

        # if buffer.typecode != 'b' and buffer.typecode != 'B':
        #     raise ValueError('image data is incorrect size')
        return [[min(StuduinoBitImage.__PIX_MAX,
                     max(StuduinoBitImage.__PIX_MIN, buffer[x]))
                 for x in range(width*y, width*(y+1))]
                for y in range(height)]

    __CREATE_IMAGE = [__default, __fromstring, __fromsize, __frombuffer]

    def __init__(self, *args, **kwargs):
        """Initialise with a string s or a buffer of width x height pixels or
        with a width and height.

        E.g.:
        Image('00000:11111:00000:11111:00000')
        Image(2, 2, array.array('b', [0,1,0,1])
        Image(3, 3)

        If no arguments are provided, initialise with 5x5 image of 0s
        """
        idx = len(args)

        if idx > 3:
            raise TypeError('function expected at most 3 arguments, got '+idx)
        self.__image = StuduinoBitImage.__CREATE_IMAGE[idx](args)
        self.__base_color = 0x1f0000
        if len(kwargs) != 0:
            if 'color' in kwargs:
                self.set_base_color(kwargs['color'])
            else:
                raise TypeError('Unexpected **kwargs: %r' % kwargs)

        self.__color = {}

    def width(self):
        """Returns the width of the image (usually 5).
        """
        return 0 if (not self.__image) else len(self.__image[0])

    def height(self):
        """Returns the height of the image (usually 5).
        """
        return len(self.__image)

    def set_pixel(self, x, y, value):
        """Set the pixel at position (x,y) to value.

        value must be between 0 and 9.
        """
        if y < 0 or x < 0 or x >= self.width() or y >= self.height():
            raise ValueError('index out of bounds')

        if(value < StuduinoBitImage.__PIX_MIN or
           value > StuduinoBitImage.__PIX_MAX):
            raise ValueError('value out of bounds')

        if value == 0:
            self.__image[y][x] = 0
        else:
            self.__image[y][x] = 1

    def __color_checker(self, color_value):
        rgb = _24bit_rgb(color_value)

        if(rgb[0] > StuduinoBitImage.__PIX_MAXCOLOR_FACTOR or
           rgb[1] > StuduinoBitImage.__PIX_MAXCOLOR_FACTOR or
           rgb[2] > StuduinoBitImage.__PIX_MAXCOLOR_FACTOR):
            return False
        if (color_value > 0x1f1f1f):
            return False
        return True

    def set_pixel_color(self, x, y, color):
        """Set the pixel at position (x,y) to value.

        value must be between 0 and 9.
        """
        if (type(color) is tuple) or (type(color) is list):
            if len(color) != 3:
                raise ValueError('color takes a (R,G,B) or [R,G,B]')
            _color = _rgb_24bit(color)
        elif (type(color) is int):
            _color = color
        else:
            raise TypeError('color takes a (R,G,B) or [R,G,B] or #RGB')

        if y < 0 or x < 0 or x >= self.width() or y >= self.height():
            raise ValueError('index out of bounds')

        if self.__color_checker(_color) is False:
            raise ValueError('color out of bounds')

        # pos = abs(x-(self.width()-1)) * self.height() + y + 1
        self.__color[(x, y)] = _color
        self.__image[y][x] = 1

    def get_pixel(self, x, y):
        """Return the value of the pixel at position (x, y).

        The value will be between 0 and 9.
        """
        if y < 0 or x < 0 or x >= self.width() or y >= self.height():
            raise ValueError('index out of bounds')

        try:
            return self.__image[y][x]
        except IndexError as e:
            raise IndexError('index out of Image')

    def get_pixel_color(self, x, y, hex=False):
        """Return the value of the pixel at position (x, y).

        The value will be between 0 and 9.
        """
        if y < 0 or x < 0 or x >= self.width() or y >= self.height():
            raise ValueError('index out of bounds')

        if self.__image[y][x] != 0:
            # pos = abs(x-(self.width()-1)) * self.height() + y + 1
            if (x, y) in self.__color.keys():
                val = self.__color[(x, y)]
            else:
                val = self.__base_color

            if hex:
                return val
            else:
                return _24bit_rgb(val)

        if hex:
            return 0
        else:
            return 0, 0, 0

    def set_base_color(self, color):
        if (type(color) is tuple) or (type(color) is list):
            if len(color) != 3:
                raise ValueError('color takes a (R,G,B) or [R,G,B]')
            _color = _rgb_24bit(color)
        elif (type(color) is int):
            _color = color
        else:
            raise TypeError('color takes a (R,G,B) or [R,G,B] or #RGB')

        if self.__color_checker(_color) is False:
            raise ValueError('color out of bounds')

        self.__base_color = _color

    def __get_base_color(self):
        return _24bit_rgb(self.__base_color)

    def shift_left(self, n):
        """Returns a new image created by shifting the image left n times.
        """
        if n < 0:
            return self.shift_right(-n)

        width = self.width()

        img = StuduinoBitImage(width, self.height())
        img.__base_color = self.__base_color

        if n < width:
            img.__image = [row[n:len(row)] + [0 for i in range(n)]
                           for row in self.__image]

            for p in self.__color.keys():
                sx = p[0]-n
                y = p[1]
                if sx >= 0:
                    img.__color[(sx, y)] = self.__color[p]

        return img

    def shift_right(self, n):
        """Returns a new image created by shifting the image right n times.
        """
        if n < 0:
            return self.shift_left(-n)

        width = self.width()

        img = StuduinoBitImage(width, self.height())
        img.__base_color = self.__base_color

        if n < width:
            img.__image = [[0 for i in range(n)] + row[0: len(row)-n]
                           for row in self.__image]

            for p in self.__color.keys():
                sx = p[0]+n
                y = p[1]
                if sx < width:
                    img.__color[(sx, y)] = self.__color[p]

        return img

    def shift_up(self, n):
        """Returns a new image created by shifting the image up n times.
        """
        if n < 0:
            return self.shift_down(-n)

        width = self.width()
        height = self.height()

        img = StuduinoBitImage(width, height)
        img.__base_color = self.__base_color

        if n < height:
            img.__image = [[x for x in row] for row in self.__image[n:height]]\
                        + [[StuduinoBitImage.__PIX_MIN for x in range(width)]
                            for y in range(n)]

            for p in self.__color.keys():
                x = p[0]
                sy = p[1]-n
                if sy >= 0:
                    img.__color[(x, sy)] = self.__color[p]

        return img

    def shift_down(self, n):
        """Returns a new image created by shifting the image down n times.
        """
        if n < 0:
            return self.shift_up(-n)

        width = self.width()
        height = self.height()

        img = StuduinoBitImage(width, height)
        img.__base_color = self.__base_color

        if n < height:
            img.__image = [[StuduinoBitImage.__PIX_MIN for x in range(width)]
                           for y in range(n)] \
                            + [[x for x in row]
                                for row in self.__image[0:height-n]]

            for p in self.__color.keys():
                x = p[0]
                sy = p[1]+n
                if sy < height:
                    img.__color[(x, sy)] = self.__color[p]

        return img

    def copy(self):
        """Returns a new image created by shifting the image right n times.
        """
        img = StuduinoBitImage(self.width(), self.height())

        img.__image = [row[0:len(row)] for row in self.__image]
        img.__base_color = self.__base_color
        img.__color = self.__color.copy()

        return img

    def __repr__(self):
        """String representation that can be eval'ed to recreate image object.

        E.g.:
        Image('10001:01010:00100:01010:10001:')
        """

        if self.__image:
            return "Image('{0}:')".format(
                ':'.join([''.join(str(r) for r in row)for row in self.__image])
                )
        else:
            return "Image('')"

    __HORI_BORDER = '-' * (__WIDTH_DEFAULT + 2)
    __VERT_BORDER = '|'
    __BODY_BORDER = __VERT_BORDER + '\n' + __VERT_BORDER
    __STR_FORMAT = '{0}\n' + __VERT_BORDER + '{1}' + __VERT_BORDER + '\n{0}'

    def __str__(self):
        """String representation of image.

        Screen top and bottom border are dashes '-'.
        Each row starts and ends with a colon ':'.
        The row of pixels is the pixel brightness with 0 replaced by a space.
        E.g.:
        -------
        |9   9|
        | 9 9 |
        |  9  |
        | 9 9 |
        |9   9|
        -------
        is the string representation of Image('90009:09090:00900:09090:90009:')
        Images too small for the 5x5 display are padded with zeroes
        to right and bottom, e.g.the string representation of Image('111:111:')
        is
        -------
        |111  |
        |111  |
        |     |
        |     |
        |     |
        -------
        Images bigger than the screen are "truncated", e.g. the string
        representation of Image('333:4444:55555:666666:7777777:88888888') is:
        -------
        |333  |
        |4444 |
        |55555|
        |66666|
        |77777|
        -------
        """

        rows = [''.join(str(e) for e in row)[:StuduinoBitImage.__WIDTH_DEFAULT]
                for row in self.__image[:StuduinoBitImage.__HEIGHT_DEFAULT]]

        vpad = StuduinoBitImage.__HEIGHT_DEFAULT - self.height()

        if vpad > 0:
            rows = rows + vpad * [' ' * StuduinoBitImage.__WIDTH_DEFAULT]

        return StuduinoBitImage.__STR_FORMAT. \
            format(StuduinoBitImage.__HORI_BORDER,
                   StuduinoBitImage.__BODY_BORDER.join(rows))

    def __add__(self, other):
        """Adding two images returns a new image that is their superimposition.
        """
        width = self.width()
        height = self.height()

        if width != other.width() or height != other.height():
            raise ValueError('Images must be the same size.')

        buf = array.array(
            'B', [min(1, self.__image[i][j] + other.__image[i][j])
                  for i in range(height) for j in range(width)]
            )

        img = StuduinoBitImage(width, height, buf)

        # change base color to individual color
        for x in range(width):
            for y in range(height):
                color1 = (0, 0, 0)
                if self.__image[y][x] != 0:
                    if (x, y) in self.__color:
                        color1 = _24bit_rgb(self.__color[(x, y)])
                    else:
                        color1 = _24bit_rgb(self.__base_color)

                color2 = (0, 0, 0)
                if other.__image[y][x] != 0:
                    if (x, y) in other.__color:
                        color2 = _24bit_rgb(other.__color[(x, y)])
                    else:
                        color2 = _24bit_rgb(other.__base_color)

                if (color1 != (0, 0, 0) or color2 != (0, 0, 0)):
                    img.__color[(x, y)] = _rgb_24bit(
                        [min(c1 + c2, StuduinoBitImage.__PIX_MAXCOLOR_FACTOR)
                         for (c1, c2) in zip(color1, color2)])

        # Add base color
        val1 = self.__get_base_color()
        val2 = other.__get_base_color()
        img.set_base_color(
            [min(v1 + v2, StuduinoBitImage.__PIX_MAXCOLOR_FACTOR)
                for v1, v2 in zip(val1, val2)])

        return img
    '''
    def __mul__(self, other):
        """Returns a new image created by multiplying the brightness of each
        pixel by n.
        """
        if other < 0:
            raise ValueError('Brightness multiplier must not be negative')

        img = self.copy()

        val = self.__get_base_color()
        # img.set_base_color(tuple(map(lambda x: int(x * other), val)))
        img.set_base_color(
            [min(v * other, StuduinoBitImage.__PIX_MAXCOLOR_FACTOR)
             for v in val])

        for key in self.__color.keys():
            # img.__color[key] = int(self.__color[key] * other)
            val = _24bit_rgb(self.__color[key])
            img.__color[key] = _rgb_24bit(
                [min(v * other, StuduinoBitImage.__PIX_MAXCOLOR_FACTOR)
                 for v in val])

        return img
    '''
    """
    def __eq__(self, other):
        if self and other:
            return self.__image == other.__image
        else:
            return not self and not other

    def __ne__(self, other):
        return not self.__eq__(other)
    """


class StuduinoBitBuiltInImage(StuduinoBitImage):
    def __init__(self, *args):
        super().__init__(*args)

    def set_pixel(self, x, y, value):
        raise TypeError("This image cannot be modified. Try copying it first.")

from .image_const1 import *
from .image_const2 import *
from .image_const3 import *
