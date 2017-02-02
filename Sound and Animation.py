# Assignment #3
# RRCC, CSC 217 470
# Programmer: Bradley Ruck
# Date Created: July 1, 2016
# Date of Final Update: July 15, 2016

# A basic Python program utilizing the Pyglet library to design a GUI complete with sounds and animation.  This program
# is designed to receive a list of 5 integers as input from user and return minimum, maximum, and average (mean) values.
# This is achieved through the use of animation and sound to help the user understand the concepts.

import pyglet
from pyglet.window import mouse

# Create the list variable to hold the 5 user inputed integer values
#
intlist = list(range(5))

# Function to sort the list in ascending order
#
def sortData(intlist) :
    # Convert elements in list to integers
    intlist = list(map(int, intlist))
    # Sort elements in list from lowest to highest
    intlist.sort()
    return intlist

# Function to identify the minimum value in list
#
def minValue(intlist) :
    return min(list(map(int, intlist)))

# Function to identify the maximum value in list
#
def maxValue(intlist) :
    return max(list(map(int, intlist)))

# Function to calculate the mean value for all the numbers in list
#
def meanValue(intlist) :
    # Calculate the sum of all 5 elements in the list
    listsum = 0
    for element in intlist :
        listsum += int(element)
    # Calculte the number of elements in the list
    listlen = len(intlist)
    # Return the mean value
    return (listsum/listlen)

# Class definition to create a rectangular box in which to hold the input widgets
#
class Rectangle(object) :
    # Draws a rectangle into a batch.
    def __init__(self, x1, y1, x2, y2, batch) :
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
                                     ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                     ('c4B', [200, 200, 220, 255] * 4)
                                     )

# Class definition to create a widget used for data input
#
class TextWidget(object) :
    def __init__(self, text, x, y, width, batch) :
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255))
                                )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y) :
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

# Class definition to create the first window that explains the program function and accepts the
# data input from the user.  This window utilizes GUI and incorporates sound in the form of 'waiting
# music', which ends after the data is entered. Exit is achieved by pressing the 'esc' key.
#
class Window(pyglet.window.Window) :
    def __init__(self, *args, **kwargs) :
        super(Window, self).__init__(800, 600, caption='Data Entry')
        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label("This is Assignment #3 - Concepts in Python",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=24,
                              x=self.width // 2, y=530,
                              anchor_x="center", anchor_y="top"),
            pyglet.text.Label("We are going to perform some simple calculations today with "
                              "your assistance. Please enter five (5) integers in any order:  ",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=12,
                              x=self.width // 2, y=370,
                              width=600,
                              anchor_x="center", anchor_y="bottom",
                              multiline='True'),
            pyglet.text.Label('Type an integer and press ENTER', x=250, y=260,
                              anchor_y='bottom', color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Integer 1', x=300, y=220, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Integer 2', x=300, y=180, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Integer 3', x=300, y=140, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Integer 4', x=300, y=100, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Integer 5', x=300, y=60, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Press ESC when finished', x=280, y=20,
                              anchor_y='bottom', color=(0, 0, 0, 255), batch=self.batch)
        ]

        # Here we create the five widget boxes that are used to accept the integer input from the user.
        #
        self.widgets = [
            TextWidget('', 400, 220, self.width - 750, self.batch),
            TextWidget('', 400, 180, self.width - 750, self.batch),
            TextWidget('', 400, 140, self.width - 750, self.batch),
            TextWidget('', 400, 100, self.width - 750, self.batch),
            TextWidget('', 400, 60, self.width - 750, self.batch)
        ]
        self.text_cursor = self.get_system_mouse_cursor('text')
        self.focus = None
        self.set_focus(self.widgets[0])

        # This is the sound player and the music selection for the 'waiting music'
        #
        self.player = pyglet.media.Player()
        waitingmusic = pyglet.resource.media('Jeopardy-theme-song.mp3')
        self.player.queue(waitingmusic)
        self.player.play()

    def on_resize(self, width, height) :
        super(Window, self).on_resize(width, height)
        for widget in self.widgets:
            widget.width = width - 110

    def on_draw(self) :
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else :
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) :
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text) :
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion) :
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion) :
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers) :
        if symbol == pyglet.window.key.ENTER:
            if modifiers & pyglet.window.key.MOD_SHIFT :
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets :
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE :
            for i in range(5):
                intlist[i] = self.widgets[i].document.text  # writes the entered values to list varaiable
            pyglet.app.exit()                               # exits the current window
            self.player.pause()                             # pauses the 'waiting music'

    def set_focus(self, focus) :
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

window1 = Window(resizable=True)
pyglet.app.run()

# Class definiton to create the second window that displays the calculation results and also utilizes
# both animation and sound to signify a successful completion of the program run. Exit is achieved by
# clicking the mouse anywhere on the open window.
#
class PrintResultsWindow(pyglet.window.Window) :
    def __init__(self):
        super(PrintResultsWindow, self).__init__(800, 600, caption = "Print Results", vsync=False)
        self.int=78
        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label("Here is the list of integers you have entered, in ascending order: ",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=55, y=500,
                              anchor_x="left", anchor_y="bottom"),
            pyglet.text.Label("Minimum integer entered: ",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=250, y=350,
                              anchor_x="left", anchor_y="bottom"),
            pyglet.text.Label("Maximum integer entered: ",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=250, y=250,
                              anchor_x="left", anchor_y="bottom",),
            pyglet.text.Label("Mean value of integers entered: ",
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=24,
                              x=110, y=100,
                              anchor_x="left", anchor_y="bottom"),
            pyglet.text.Label(str(sortData(intlist)),
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=320, y=450,
                              anchor_x="left", anchor_y="bottom"),
            pyglet.text.Label(str(minValue(intlist)),
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=550, y=350,
                              anchor_x="left", anchor_y="bottom"),
            pyglet.text.Label(str(maxValue(intlist)),
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=18,
                              x=550, y=250,
                              anchor_x="left", anchor_y="bottom", ),
            pyglet.text.Label(str(meanValue(intlist)),
                              color=(0, 0, 0, 255), batch=self.batch,
                              font_size=24,
                              x=610, y=100,
                              anchor_x="left", anchor_y="bottom")
             ]

    # Here both animaiton and sound are utilized to signify successful completion of program run.
    #
    fireworkssound = pyglet.media.load('Fireworks Finale.mp3', streaming=False)
    looper = pyglet.media.SourceGroup(fireworkssound.audio_format, None)
    looper.loop = True
    looper.queue(fireworkssound)
    p = pyglet.media.Player()
    p.queue(looper)
    p.play()

    fireworks = pyglet.resource.animation('fireworks1.gif')
    sprite1 = pyglet.sprite.Sprite(fireworks, x=50, y=380)
    fireworks = pyglet.resource.animation('fireworks2.gif')
    sprite2 = pyglet.sprite.Sprite(fireworks, x=50, y=50)
    fireworks = pyglet.resource.animation('fireworks3.gif')
    sprite3 = pyglet.sprite.Sprite(fireworks, x=500, y=350)
    fireworks = pyglet.resource.animation('fireworks4.gif')
    sprite4 = pyglet.sprite.Sprite(fireworks, x=480, y=130)

    def on_draw(self) :
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()
        self.sprite1.draw()
        self.sprite2.draw()
        self.sprite3.draw()
        self.sprite4.draw()

    # This allows for app termination on mouse click anywhere on open window
    #
    def on_mouse_press(self, x, y, button, modifiers) :
        if button == mouse.LEFT:
            pyglet.app.exit()

window2 = PrintResultsWindow()
pyglet.app.run()
