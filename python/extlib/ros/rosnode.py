try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import rospy

try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import sys


class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Ros Node", "extlib.ros.rosnode", {"name": "graphex"},
                                   {},
                                   {},
                                   "Create a ros node.", verbose, needs_foreground=True)
        self.args = args
        self.isinit = False
        self.rate = None

    def tick(self, value):
        if not self.isinit:
            rospy.init_node(self.args["name"], anonymous=False)
            self.rate = rospy.Rate(50) # 10hz
            self.isinit = True
            builtins.shutdown_hook.append(self.shutdown_ros)
        #self.rate.sleep()
        #rospy.spinOnce()
        
        return {}

    def shutdown_ros(self):
        rospy.signal_shutdown("Graph execution stopped.")
        print("Shutting down ros.")
        sys.stdout.flush()