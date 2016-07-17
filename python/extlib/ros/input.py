try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import rospy
import time


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Listen", "extlib.ros.input", {"rate": 10, "topic": "/test", "code": 'from std_msgs.msg import String as topic_type'},
                                   {},
                                   {"result": "Object"},
                                   "Listen on topic.", verbose, isInput=True, isRepeating=True)
        self.args = args
        self.initialized = False
        self.data = None

    def listen_callback(self, data):
      self.data = data
        
    def tick(self, value):
        tag = None
        result = []
        
        if not self.initialized:
            exec(self.args["code"])
            rospy.Subscriber(self.args["topic"], topic_type, self.listen_callback)
            
        sleep_time = 1.0/self.args["rate"]
        time.sleep(sleep_time)

        result = self.data
        self.data = None

        if tag:
            return {"result": result, "tags": {"result": tag}}
        else:
            return {"result": result}
