'''
Created on 16.07.2015

@author: Michael Fuerst
@version: 1.0
'''

import time
from time import sleep
from threading import Thread

try:
    import extlib.raspi.Adafruit_PWM_Servo_Driver as servoDriver
except ImportError:
    import extlib.raspi.Dummy_PWM_Servo_Driver as servoDriver
try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("RcCar", "raspi.rccar",
                                   {"maxSpeed": 0.5},
                                   {"speed": "Number", "turn": "Number"},
                                   {},
                                   "Set turn and speed of rccar.", verbose)
        self.args = args
        self.driver = None

    def tick(self, value):
        if self.driver is None:
            self.driver = BareDriver()
            Thread(target=self.driver.driveloop).start()
            self.driver.setMax(self.args["maxSpeed"])
        self.driver.set(value["speed"], value["turn"])
        return {}


class BareDriver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.pwm = servoDriver.PWM(0x40)
        self.real_steering = 1350
        self.real_speed = 1600
        self.location = None

        print("Initializing Hardware.")

        self.maxSpeed = 1.0
        self.speed = 0.0
        self.steering = -1.0
        self.applySpeedAndSteering(True)
        sleep(2.0)

        self.maxSpeed = 1.0
        self.speed = 1.0
        self.steering = 0.0
        self.applySpeedAndSteering(True)
        sleep(1.0)

        self.maxSpeed = 1.0
        self.speed = -1.0
        self.steering = 1.0
        self.applySpeedAndSteering(True)
        sleep(1.0)

        self.maxSpeed = 0.1
        self.speed = 0.0
        self.steering = 0.0
        self.applySpeedAndSteering(True)

        print("Initialized Hardware.")

        self.lastKeepAlive = time.time() - 1.0

    def applySpeedAndSteering(self, instant=False):
        speed = 1600.0 + 1000.0 * self.speed * self.maxSpeed  # 200 +- 100
        steering = 1350.0 - 200.0 * self.steering  # 400+-100

        if instant:
            self.real_speed = speed
            self.real_steering = steering

        if (self.real_speed < speed):
            self.real_speed += 10
        elif (self.real_speed > speed):
            self.real_speed -= 10

        if (self.real_steering < steering):
            self.real_steering += 10
        elif (self.real_steering > steering):
            self.real_steering -= 10

        # Set speed with dead pwm if exactly 0 is set.
        if self.speed == 0.0:
            self.pwm.setPWM(1, 0, 0)
        else:
            self.pwm.setPWM(1, 0, int(self.real_speed))
        # Set steering with dead pwm if exactly 0 is set.
        if self.steering == 0.0:
            self.pwm.setPWM(0, 0, 0)
        else:
            self.pwm.setPWM(0, 0, int(self.real_steering))

    def set(self, speed, turn):
        self.speed = speed
        self.steering = turn
        self.lastKeepAlive = time.time()

    def setMax(self, speed):
        self.maxSpeed = speed

    def drive(self):
        cur = time.time()
        if cur - self.lastKeepAlive > 1.0:
            self.speed = 0.0
            self.steering = 0.0

        self.applySpeedAndSteering()

        elapsed = time.time() - cur
        if elapsed < 0.05:
            sleep(0.05 - elapsed)

    def driveloop(self):
        while True:
            self.drive()


def instance(verbose, args):
    return Node(verbose, args)


if __name__ == "__main__":
    print("A node.")
