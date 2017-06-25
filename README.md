# tscrnsvr

Screensavers and other goodies for the terminal.
![screensaver gif](http://i.imgur.com/0H2cOic.gif)

## Installation

Python3 must be used. This was tested on 3.6, but uses no 3.6-specific features. It should work on other versions.
```
pip install tscrnsvr
```

## Usage

```
> /usr/bin/tscrnsvr --help

usage: tscrnsvr [-h]
                {bounce,clock,colortest,imgbounce,matrix,pipes,snake,stars}
                ...

positional arguments:
  {bounce,clock,colortest,imgbounce,matrix,pipes,snake,stars}
    bounce              Bounce text around your terminal.
    clock               A simple digital clock. Requires FIGlet to be
                        installed.
    colortest           Displays color palette.
    imgbounce           Bounce an image around your terminal.
    matrix              A screensaver like the one in the movie "The Matrix"
    pipes               Screensaver similar to that of Windows XP; only 2D.
    snake               Play snake!
    stars               Make "stars" fly across your screen.

optional arguments:
  -h, --help            show this help message and exit
```

### ```bounce```: Bounce text around the terminal
```
usage: tscrnsvr bounce [-h] [-c COLOR] [-d DELAY] [-g] [-s] [-S STRING]

optional arguments:
  -h, --help            show this help message and exit
  -c COLOR, --color COLOR
                        set color of text (default 15)
  -d DELAY, --delay DELAY
                        set delay between frames in seconds (default 0.1)
  -g, --debug           show debug statistics in upper left corner
  -s, --screensaver     screensaver mode (press any key to leave)
  -S STRING, --string STRING
                        set string for bounce
```

### ```clock```: A simple digital clock.
***Requires [FIGlet](http://www.figlet.org/) ---
```
usage: tscrnsvr clock [-h] [-bc BOTTOMCOLOR] [-bs BOTTOMSTRF] [-f FONT] [-g]
                      [-s] [-tc TOPCOLOR] [-ts TOPSTRF]

optional arguments:
  -h, --help            show this help message and exit
  -bc BOTTOMCOLOR, --bottomcolor BOTTOMCOLOR
                        set color for bottom text (default 15)
  -bs BOTTOMSTRF, --bottomstrf BOTTOMSTRF
                        string to be passed to time.strftime() for the bottom
                        text (default "%A, %B %d, %Y")
  -f FONT, --font FONT  set FIGlet font that the digital clock should display
                        (defaults to banner)
  -g, --debug           show debug statistics in upper left corner
  -s, --screensaver     run in screensaver mode (press any key to exit)
  -tc TOPCOLOR, --topcolor TOPCOLOR
                        set color for top text (default 15)
  -ts TOPSTRF, --topstrf TOPSTRF
                        string to be passed to time.strftime() for the top
                        text (default "%I:%M:%S %p")
```
### ```imgbounce```: Bounce an image around the terminal.
```
usage: tscrnsvr imgbounce [-h] [-d DELAY] [-g] [-s] [-x DIMENSIONS] image

positional arguments:
  image                 set image for bounce

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        set delay between frames in seconds (default 0.1)
  -g, --debug           show debug statistics in upper left corner
  -s, --screensaver     screensaver mode (press any key to leave)
  -x DIMENSIONS, --dimensions DIMENSIONS
                        dimensions for image to bounce (default 32x32)
```
### ```matrix```: _Matrix_-like screensaver
```
usage: tscrnsvr matrix [-h] [-c COLORS] [-C CHARS] [-cc HEADCOLOR] [-d DELAY]
                       [-g] [-miln MINLENGTH] [-milt MINLIFETIME]
                       [-mis MINSPEED] [-mxln MAXLENGTH] [-mxlt MAXLIFETIME]
                       [-mxs MAXSPEED] [-n FADES] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c COLORS, --colors COLORS
                        set fade colors. Must be a comma separated list of
                        values on the terminal's color palette. (default
                        83,84,119,120)
  -C CHARS, --chars CHARS
                        set fade characters. Is a comma separated list of
                        unicode ranges. Can be one character or a range.
                        [Example: -C 32-55,66,2605,2606,6785-8941] (default
                        32-128)
  -cc HEADCOLOR, --headcolor HEADCOLOR
                        set color of the first character of every fade.
  -d DELAY, --delay DELAY
                        set delay between frames in seconds (default 0.1)
  -g, --debug           show debug statistics in upper left corner
  -miln MINLENGTH, --minlength MINLENGTH
                        set minimum length of fades (default 4)
  -milt MINLIFETIME, --minlifetime MINLIFETIME
                        set minimum lifetime of fades (default 10)
  -mis MINSPEED, --minspeed MINSPEED
                        set minimum speed of fades (default 0.5)
  -mxln MAXLENGTH, --maxlength MAXLENGTH
                        set maximum length of fades (default 20)
  -mxlt MAXLIFETIME, --maxlifetime MAXLIFETIME
                        set maximum lifetime of fades (default 30)
  -mxs MAXSPEED, --maxspeed MAXSPEED
                        set maximum speed of fades (default 2)
  -n FADES, --fades FADES
                        set number of "fades" on screen (default 25)
  -s, --screensaver     screensaver mode (press any key to leave)
```
### ```pipes```: Mimics WinXP screensaver of the same name
```
usage: tscrnsvr pipes [-h] [-c COLORS] [-C STYLE] [-d DELAY] [-g] [-n PIPES]
                      [-r RSTIME] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c COLORS, --colors COLORS
                        set pipe colors. Must be a comma separated list of
                        values on the terminal's color palette. (default
                        random choice)
  -C STYLE, --style STYLE
                        set pipe style. Non-zero integer up to 4.
  -d DELAY, --delay DELAY
                        set delay between frames in seconds (default 0.1)
  -g, --debug           show debug statistics in upper left corner
  -n PIPES, --pipes PIPES
                        set number of pipes on screen (default 10)
  -r RSTIME, --rstime RSTIME
                        restart pipe system every RSTIME frames. (default 200)
  -s, --screensaver     screensaver mode (press any key to leave)
```
### ```snake```: Play snake!
```
usage: tscrnsvr snake [-h] [-C CHAR] [-c COLOR] [-d DELAY] [-F FRUITCHAR]
                      [-f FRUITCOLOR] [-l STARTLENGTH]

optional arguments:
  -h, --help            show this help message and exit
  -C CHAR, --char CHAR  set code of the character for the snake's head and
                        body (default 64)
  -c COLOR, --color COLOR
                        set color for snake
  -d DELAY, --delay DELAY
                        delay between each frame (default 0.1)
  -F FRUITCHAR, --fruitchar FRUITCHAR
                        set character for fruit (default 65)
  -f FRUITCOLOR, --fruitcolor FRUITCOLOR
                        set color for fruit (default 125)
  -l STARTLENGTH, --startlength STARTLENGTH
                        set starting length of snake
```
### ```stars```: Space flight simulator.
```
usage: tscrnsvr stars [-h] [-a ACCELERATION] [-c COLORS] [-C CHARS] [-d DELAY]
                      [-g] [-q CHANCE] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -a ACCELERATION, --acceleration ACCELERATION
                        Acceleration rate of stars (default 0.3)
  -c COLORS, --colors COLORS
                        set star colors. Must be a comma separated list of
                        values on the terminal's color palette. (default 227)
  -C CHARS, --chars CHARS
                        set star characters. Is a comma separated list of
                        unicode ranges. Can be one character or a range.
                        [Example: -C 32-55,66,2605,2606,6785-8941] (default
                        42)
  -d DELAY, --delay DELAY
                        set delay between frames in seconds (default 0.01)
  -g, --debug           show debug statistics in upper left corner
  -q CHANCE, --chance CHANCE
                        Chance for a star to spawn each frame (default 0.2)
  -s, --screensaver     screensaver mode (press any key to leave)
```