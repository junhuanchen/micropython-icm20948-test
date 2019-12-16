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
from image import StuduinoBitImage as Image
from machine import Pin
from neopixel import NeoPixel
import time
import _thread
from const import *
from common import _rgb_24bit, _24bit_rgb


# for singleton pattern
# Implement used global value,
# maybe Micropython 'function' object can't have attribute...
__display = None


def get_display_object():
    global __display

    from dsply import __SBDisplay

    if __display is None:
        __display = __SBDisplay()
    return __display


class StuduinoBitDisplay(BuiltinColor):
    def __init__(self):
        self.__display = get_display_object()

    def get_pixel(self, x, y):
        return self.__display.get_pixel(x, y)

    def set_pixel(self, x, y, color):
        self.__display.set_pixel(x, y, color)

    def clear(self):
        self.__display.clear()

    def show(self, iterable, delay=400, *,
             wait=True, loop=False, clear=False, color=None):
        self.__display.show(iterable, delay=delay, wait=wait,
                            loop=loop, clear=clear, color=color)

    def scroll(self, string, delay=150, *,
               wait=True, loop=False, monospace=False, color=None):
        self.__display.scroll(string, delay=delay, wait=wait, loop=loop,
                              monospace=monospace, color=color)

    def on(self):
        self.__display.on()

    def off(self):
        self.__display.off()

    def is_on(self):
        return self.__display.is_on()


""" ---------------------------------------------------------------------- """
""" The LED display ------------------------------------------------------ """


class __SBDisplay(BuiltinColor):
    """Display class represents the 5x5 LED display.

    There is a single display object that has an image.
    """
    __PIX_MAXCOLOR_FACTOR = 31

    def __init__(self):
        """Initialise the display.
        """
        self.__last_image = Image(5, 5)

        self.__powerPin = Pin(2, Pin.OUT)
        self.__controlPin = Pin(4, Pin.OUT)
        self.__np = NeoPixel(self.__controlPin, 25)
        self.__np.fill((0, 0, 0))
        self.__powerPin.value(True)
        self.__on = True

        self.__bgthid = -1

    def __print(self, image, color):
        """Output to the display.
        """
        for x in range(image.width()):
            for y in range(image.height()):
                val = image.get_pixel_color(x, y)
                if (val != (0, 0, 0)) and (color is not None):
                    val = color
                pos = abs(x-4) * 5 + y
                self.__np[pos] = val
        self.__np.write()

    def get_pixel(self, x, y):
        """Gets the brightness of LED pixel (x,y).

        Brightness can be from 0 (LED is off) to 9 (maximum LED brightness).
        """
        if y < 0 or x < 0 or y > 4 or x > 4:
            raise ValueError('index out of bounds')

        pos = abs(x-4) * 5 + y
        val = self.__np[pos]
        return val

    def set_pixel(self, x, y, color):
        """Set the dsplay at LED pixel (x,y) to color.
            """
        if (type(color) is tuple) or (type(color) is list):
            val = color
        elif (type(color) is int):
            val = _24bit_rgb(color)
        else:
            raise TypeError('color takes a (R,G,B) or [R,G,B] or #RGB')

        if y < 0 or x < 0 or y > 4 or x > 4:
            raise ValueError('index out of bounds')

        if(val[0] < 0 or val[0] > __SBDisplay.__PIX_MAXCOLOR_FACTOR or
           val[1] < 0 or val[1] > __SBDisplay.__PIX_MAXCOLOR_FACTOR or
           val[2] < 0 or val[2] > __SBDisplay.__PIX_MAXCOLOR_FACTOR):
            raise ValueError('color factor must be 0-{0}'.
                             format(__SBDisplay.__PIX_MAXCOLOR_FACTOR))

        pos = abs(x-4) * 5 + y
        self.__np[pos] = val
        self.__np.write()
        time.sleep_ms(1)

    def clear(self):
        """Clear the display.
        """
        if self.__bgthid != -1:
            self.__bgthid = -1

        self.__last_image = Image(5, 5)
        self.__np.fill((0, 0, 0))
        self.__np.write()

    def show(self, iterable, delay=400, *,
             wait=True, loop=False, clear=False, color=None):
        if wait:
            if loop:
                self.__show_loop(iterable, delay=delay,
                                 clear=clear, color=color)
            else:
                self.__one_show(iterable, delay=delay,
                                clear=clear, color=color)
        else:
            if loop:
                _thread.start_new_thread(self.__show_loop, (iterable, delay),
                                         {'clear': clear, 'color': color})
            else:
                _thread.start_new_thread(self.__one_show, (iterable, delay),
                                         {'clear': clear, 'color': color})

    def __show_loop(self, iterable, delay, *, clear=False, color=None):
        while True:
            self.__one_show(iterable, delay=delay, clear=clear, color=color)

    def __one_show(self, iterable, delay, *, clear=False, color=None):
        """Show images or a string on the display.

        Shows the images an image at a time or a string a character at a time,
        with delay milliseconds between image/character.
        If loop is True, loop forever.
        If clear is True, clear the screen after showing.
        Usage:
        shows an image:
        display.show(image, delay=0, wait=True, loop=False, clear=False)
        show each image or letter in the iterable:
        display.show(iterable, delay=400, wait=True, loop=False, clear=False)
        """
        if iterable is None:
            raise TypeError('not iterable')

        if not iterable:
            return

        val = color
        if (type(color) is tuple) or (type(color) is list):
            val = color
        elif (type(color) is int):
            val = _24bit_rgb(color)
        elif color is not None:
            raise TypeError('color takes a (R,G,B) or [R,G,B] or #RGB')

        if isinstance(iterable, str):
            iterable = [Image(Image.CHARACTER_MAP.
                        get(c, Image.CHARACTER_MAP.get('?')))
                        for c in iterable]

        if isinstance(iterable, Image):
            iterable = [iterable]

        for img in iterable:
            # if img != self.__last_image:
            self.__print(img, val)
            self.__last_image = img
            time.sleep_ms(delay)

        if clear:
            self.clear()

    def scroll(self, string, delay=150, *,
               wait=True, loop=False, monospace=False, color=None):
        if wait:
            if loop:
                self.__scroll_loop(string, delay=delay,
                                   monospace=monospace, color=color)
            else:
                self.__one_scroll(string, delay=delay,
                                  monospace=monospace, color=color)
        else:
            if loop:
                _thread.start_new_thread(self.__scroll_loop, (string, delay),
                                         {'monospace': monospace,
                                         'color': color})
            else:
                _thread.start_new_thread(self.__one_scroll, (string, delay),
                                         {'monospace': monospace,
                                         'color': color})

    def __scroll_loop(self, string, delay, *, monospace, color):
        while True:
            self.__one_scroll(string, delay=delay,
                              monospace=monospace, color=color)

    def __one_scroll(self, string, delay, *, monospace, color):
        """Scroll the string across the display with given delay.

        In this emulation this is the same as showing the string and clearing
        the screen.
        """
        # _thread.allowsuspend(True)

        if not isinstance(string, str):
            raise TypeError('can\'t convert ', type(string),
                            'to str implicitly')

        val = color
        if (type(color) is tuple) or (type(color) is list):
            val = color
        elif (type(color) is int):
            val = _24bit_rgb(color)
        elif color is not None:
            raise TypeError('color takes a (R,G,B) or [R,G,B] or #RGB')

        disp_string = ' ' + string + ' '
        for i in range(len(disp_string)-1):
            curr = Image(Image.CHARACTER_MAP.get(disp_string[i],
                         Image(Image.CHARACTER_MAP.get('?'))))
            next = Image(Image.CHARACTER_MAP.get(disp_string[i+1],
                         Image(Image.CHARACTER_MAP.get('?'))))
            for i in range(5):
                time.sleep_ms(delay)
                bc = curr.__get_base_color()
                img = curr.shift_left(i) + next.shift_right(5-i)
                img.set_base_color(bc)

                self.__print(img, val)
                time.sleep_ms(delay)

        self.clear()

    def on(self):
        if self.__on:
            return
        self.__on = True
        self.__powerPin.value(self.__on)
        self.show(self.__last_image)

    def off(self):
        for x in range(5):
            for y in range(5):
                val = self.get_pixel(x, y)
                self.__last_image.set_pixel_color(x, y, val)

        self.__on = False
        self.__powerPin.value(self.__on)

    def is_on(self):
        return self.__on
