try:
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import rospy

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Publish", "extlib.ros.output", {"topic": "/test", "code": 'from std_msgs.msg import String as topic_type'},
                                   {"val": "Object"},
                                   {},
                                   "Publish on topic.", verbose)
        self.args = args
        self.pub = None

    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        val = value["val"]
        
        if self.pub is None:
            exec(self.args["code"])
            self.pub = rospy.Publisher(self.args["topic"], topic_type, queue_size=1)

        self.pub.publish(val)

        return {}
