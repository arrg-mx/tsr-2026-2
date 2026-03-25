#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class SubNode(Node):
    def __init__(self):
        super().__init__('subcriber_node')

        self.counter_ = 0

        self.subcriber_ = self.create_subscription(
            msg_type= Int64,
            topic="publiser_topic", 
            callback=self.sub_cbk, qos_profile= 10)
        
        self.publisher_ = self.create_publisher(
            msg_type= Int64, 
            topic= 'counter_topic', 
            qos_profile= 10)
        
        self.get_logger().info("Nodo subscritor activo")


    def sub_cbk(self, msg):
        self.counter_ += msg.data

        new_mesg = Int64()
        new_mesg._data = self.counter_

        # self.get_logger().info("Conteo igual a " + str(self.counter_))
        self.publisher_.publish(new_mesg)


def main(args = None):
    rclpy.init(args=args)
    node = SubNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
