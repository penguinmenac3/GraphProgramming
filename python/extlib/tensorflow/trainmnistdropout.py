try: 
    from ...stdlib import Node as base
except ValueError:
    from stdlib import Node as base
import random
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import sys

class Node(base.Node):
    def __init__(self, verbose, args):
        super(Node, self).__init__("Train MNIST (dropout)", "extlib.tensorflow.trainmnistdropout", {},
                                   {"session":"TFSession", "train_step": "Tensor", "x": "Tensor", "y": "Tensor", "y_": "Tensor", "keep_prob": "Tensor"},
                                   {"session": "TFSession", "accuracy": "Number", "iteration": "Number"},
                                   "Trains the net on mnist.", verbose, needs_foreground=True)
        self.args = args
        self.max_iterations = 20000
        self.iteration = 0
        
        self.mnist = None
        self.accuracy = None

    def isRepeating(self):
        return self.iteration < self.max_iterations
      
    def tick(self, value):
        tag = None
        if "tags" in value and "val" in value["tags"]:
            tag = value["tags"]["val"]
        
        train_step = value["train_step"]
        x = value["x"]
        y = value["y"]
        y_ = value["y_"]
        keep_prob = value["keep_prob"]
        session = value["session"]
        train_accuracy = 0
        calculated_accuracy = None

        if self.accuracy is None:
        	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        	self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        if self.mnist is None:
        	self.mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

        if self.iteration < self.max_iterations:
            batch = self.mnist.train.next_batch(50)
            if self.iteration%10 == 0:
                calculated_accuracy = float(session.run(self.accuracy, feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0}))
            session.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
            session = None
        else:
            calculated_accuracy = float(session.run(self.accuracy, feed_dict={x: self.mnist.test.images, y_: self.mnist.test.labels, keep_prob: 1.0}))
        self.iteration = self.iteration + 1
        
        if tag:
            return {"session": session,"accuracy": calculated_accuracy,"iteration": self.iteration, "tags":{"result":tag,"accuracy": tag,"iteration": tag}}
        else:
            return {"session": session,"accuracy": calculated_accuracy,"iteration": self.iteration}
