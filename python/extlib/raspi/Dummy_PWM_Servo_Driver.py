# -*- coding: utf-8 -*-
#!/usr/bin/python

import math

# ============================================================================
# A dummy servo driver.
# ============================================================================


class PWM:

    @classmethod
    def softwareReset(cls):
        "Sends a software reset (SWRST) command to all the servo drivers on the bus"
        print("Softwarereset.")

    def __init__(self, address=0x40, debug=False):
        self.debug = debug
        print("Initialized dummy servo driver.")

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)

        print("Set frequency to %d" % freq)

    def setAllPWM(self, on, off):
        if (self.debug):
            print("Set all pwm channels to %d on and %d off" % (on, off))

    def setPWM(self, channel, on, off):
        if (self.debug):
            print("Set pwm channel %d to %d on and %d off" % (channel, on, off))
