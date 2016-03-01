try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base

import RPi.GPIO as GPIO
import time
import numbers

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("GPIO In", "raspberrypi.gpioin", 10, {},
                                   {"result": "Boolean"},
                                   "Read if a gpio has a signal.", verbose, True, True)
        self.args = args
        self.state = False
        if  isinstance(self.args, numbers.Number):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(self.args, GPIO.IN)
            self.state = (GPIO.input(self.args) == 1)

    def tick(self, value):
        while (GPIO.input(self.args) == 1) is self.state:
            time.sleep(0.001)
        return {"result": self.state}
