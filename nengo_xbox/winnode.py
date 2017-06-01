import nengo
import numpy as np

from . import windows

from operator import itemgetter, attrgetter

class Xbox(nengo.Network):
    axis_names = ['l_thumb_x', 'l_thumb_y',
                  'r_thumb_x', 'r_thumb_y',
                  'left_trigger', 'right_trigger']

    def __init__(self, label=None, index=0):
        super(Xbox, self).__init__(label=label)

        self.index = index
        self.j = self.create_joystick(index)

        self.button_values = np.zeros(16)
        @self.j.event
        def on_button(button, pressed):
            self.button_values[button-1] = pressed

        self.axis_values = np.zeros(6)
        @self.j.event
        def on_axis(axis, value):
            index = Xbox.axis_names.index(axis)
            if index < 4:
                value = value * 2  # use full range -1.0 to 1.0
            self.axis_values[index] = value

        with self:
            self.update = nengo.Node(lambda t: self.j.dispatch_events())
            self.buttons = nengo.Node(lambda t: self.button_values)
            self.axis = nengo.Node(lambda t: self.axis_values)

            self.vibrate = nengo.Node(lambda t, x: self.j.set_vibration(*x),
                                      size_in=2)

    def create_joystick(self, index):
        joysticks = windows.XInputJoystick.enumerate_devices()
        return joysticks[index]




