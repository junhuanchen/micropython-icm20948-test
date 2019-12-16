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
from .image import StuduinoBitBuiltInImage

""" Built-in images and character map """

ANGRY = StuduinoBitBuiltInImage('90009:09090:00000:99999:90909:')
ASLEEP = StuduinoBitBuiltInImage('00000:99099:00000:09990:00000:')
BUTTERFLY = StuduinoBitBuiltInImage('99099:99999:00900:99999:99099:')
CHESSBOARD = StuduinoBitBuiltInImage('09090:90909:09090:90909:09090:')
CONFUSED = StuduinoBitBuiltInImage('00000:09090:00000:09090:90909:')
COW = StuduinoBitBuiltInImage('90009:90009:99999:09990:00900:')
DIAMOND = StuduinoBitBuiltInImage('00900:09090:90009:09090:00900:')
DIAMOND_SMALL = StuduinoBitBuiltInImage('00000:00900:09090:00900:00000:')
DUCK = StuduinoBitBuiltInImage('09900:99900:09999:09990:00000:')
FABULOUS = StuduinoBitBuiltInImage('99999:99099:00000:09090:09990:')
GHOST = StuduinoBitBuiltInImage('99999:90909:99999:99999:90909:')
GIRAFFE = StuduinoBitBuiltInImage('99000:09000:09000:09990:09090:')
HAPPY = StuduinoBitBuiltInImage('00000:09090:00000:90009:09990:')
HEART = StuduinoBitBuiltInImage('09090:99999:99999:09990:00900:')
HEART_SMALL = StuduinoBitBuiltInImage('00000:09090:09990:00900:00000:')
HOUSE = StuduinoBitBuiltInImage('00900:09990:99999:09990:09090:')
MEH = StuduinoBitBuiltInImage('09090:00000:00090:00900:09000:')
MUSIC_CROTCHET = StuduinoBitBuiltInImage('00900:00900:00900:99900:99900:')
MUSIC_QUAVER = StuduinoBitBuiltInImage('00900:00990:00909:99900:99900:')
MUSIC_QUAVERS = StuduinoBitBuiltInImage('09999:09009:09009:99099:99099:')
NO = StuduinoBitBuiltInImage('90009:09090:00900:09090:90009:')
PACMAN = StuduinoBitBuiltInImage('09999:99090:99900:99990:09999:')
PITCHFORK = StuduinoBitBuiltInImage('90909:90909:99999:00900:00900:')
RABBIT = StuduinoBitBuiltInImage('90900:90900:99990:99090:99990:')
ROLLERSKATE = StuduinoBitBuiltInImage('00099:00099:99999:99999:09090:')
SAD = StuduinoBitBuiltInImage('00000:09090:00000:09990:90009:')
SILLY = StuduinoBitBuiltInImage('90009:00000:99999:00909:00999:')
SKULL = StuduinoBitBuiltInImage('09990:90909:99999:09990:09990:')
SMILE = StuduinoBitBuiltInImage('00000:00000:00000:90009:09990:')
SNAKE = StuduinoBitBuiltInImage('99000:99099:09090:09990:00000:')
SQUARE = StuduinoBitBuiltInImage('99999:90009:90009:90009:99999:')
SQUARE_SMALL = StuduinoBitBuiltInImage('00000:09990:09090:09990:00000:')
STICKFIGURE = StuduinoBitBuiltInImage('00900:99999:00900:09090:90009:')
SURPRISED = StuduinoBitBuiltInImage('09090:00000:00900:09090:00900:')
SWORD = StuduinoBitBuiltInImage('00900:00900:00900:09990:00900:')
TARGET = StuduinoBitBuiltInImage('00900:09990:99099:09990:00900:')
TORTOISE = StuduinoBitBuiltInImage('00000:09990:99999:09090:00000:')
TRIANGLE = StuduinoBitBuiltInImage('00000:00900:09090:99999:00000:')
TRIANGLE_LEFT = StuduinoBitBuiltInImage('90000:99000:90900:90090:99999:')
TSHIRT = StuduinoBitBuiltInImage('99099:99999:09990:09990:09990:')
UMBRELLA = StuduinoBitBuiltInImage('09990:99999:00900:90900:09900:')
XMAS = StuduinoBitBuiltInImage('00900:09990:00900:09990:99999:')
YES = StuduinoBitBuiltInImage('00000:00009:00090:90900:09000:')

ARROW_N = StuduinoBitBuiltInImage('00900:09990:90909:00900:00900:')
ARROW_NE = StuduinoBitBuiltInImage('00999:00099:00909:09000:90000:')
ARROW_E = StuduinoBitBuiltInImage('00900:00090:99999:00090:00900:')
ARROW_SE = StuduinoBitBuiltInImage('90000:09000:00909:00099:00999:')
ARROW_S = StuduinoBitBuiltInImage('00900:00900:90909:09990:00900:')
ARROW_SW = StuduinoBitBuiltInImage('00009:00090:90900:99000:99900:')
ARROW_W = StuduinoBitBuiltInImage('00900:09000:99999:09000:00900:')
ARROW_NW = StuduinoBitBuiltInImage('99900:99000:90900:00090:00009:')

CLOCK12 = StuduinoBitBuiltInImage('00900:00900:00900:00000:00000:')
CLOCK1 = StuduinoBitBuiltInImage('00090:00090:00900:00000:00000:')
CLOCK2 = StuduinoBitBuiltInImage('00000:00099:00900:00000:00000:')
CLOCK3 = StuduinoBitBuiltInImage('00000:00000:00999:00000:00000:')
CLOCK4 = StuduinoBitBuiltInImage('00000:00000:00900:00099:00000:')
CLOCK5 = StuduinoBitBuiltInImage('00000:00000:00900:00090:00090:')
CLOCK6 = StuduinoBitBuiltInImage('00000:00000:00900:00900:00900:')
CLOCK7 = StuduinoBitBuiltInImage('00000:00000:00900:09000:09000:')
CLOCK8 = StuduinoBitBuiltInImage('00000:00000:00900:99000:00000:')
CLOCK9 = StuduinoBitBuiltInImage('00000:00000:99900:00000:00000:')
CLOCK10 = StuduinoBitBuiltInImage('00000:99000:00900:00000:00000:')
CLOCK11 = StuduinoBitBuiltInImage('09000:09000:00900:00000:00000:')

ALL_ARROWS = [
    ARROW_N,
    ARROW_NE,
    ARROW_E,
    ARROW_SE,
    ARROW_S,
    ARROW_SW,
    ARROW_W,
    ARROW_NW,
    ]

ALL_CLOCKS = [
    CLOCK12,
    CLOCK1,
    CLOCK2,
    CLOCK3,
    CLOCK4,
    CLOCK5,
    CLOCK6,
    CLOCK7,
    CLOCK8,
    CLOCK9,
    CLOCK10,
    CLOCK11,
    ]
