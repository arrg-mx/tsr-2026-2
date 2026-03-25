#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class MyNode(Node):
    def __init__(self):
        super().__init__("my_node")
        self.number_ = 2

        self.publisher_ = self.create_publisher(
            msg_type= Int64,topic= "publiser_topic",
              qos_profile= 10)

        self.timer_ = self.create_timer(
            timer_period_sec= 2.0,
              callback= self.cbck)

        self.get_logger().info("Primer nodo activo")

    def cbck(self):
        msg = Int64()
        msg.data = self.number_
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()




