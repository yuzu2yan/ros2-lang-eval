#!/usr/bin/env python3
"""
ROS2 Python node that acts as a 'pong' for latency benchmarks.
It subscribes to a 'ping' topic and immediately republishes the message
to a 'pong' topic. This is used to measure round-trip time.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

class PythonBenchmarkNode(Node):
    """A node that republishes PointCloud2 messages for benchmarking."""

    def __init__(self):
        super().__init__('python_benchmark_node')
        
        # Create a publisher for the pong topic
        self.publisher_ = self.create_publisher(PointCloud2, 'pong_python', 10)
        
        # Create a subscriber to the ping topic
        self.subscription = self.create_subscription(
            PointCloud2,
            'ping',
            self.pong_callback,
            10)
        
        self.get_logger().info('Python Pong Node for PointCloud2 benchmark started.')

    def pong_callback(self, msg):
        """Receives a message and immediately republishes it."""
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PythonBenchmarkNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()