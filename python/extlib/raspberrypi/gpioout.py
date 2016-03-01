try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import RPi.GPIO as GPIO
import numbers

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("GPIO Out", "raspberrypi.gpioout", 8, {"val": "Boolean"},
                                   {},
                                   "Set the gpio pin to the input value", verbose, False, False)
        self.args = args
        if isinstance(self.args, numbers.Number):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(self.args, GPIO.OUT)
            GPIO.output(self.args, False)

    def tick(self, value):
        GPIO.output(self.args, value["val"])
        return {}
