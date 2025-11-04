#!/usr/bin/env python3
"""
Python benchmark node for ROS2 performance comparison.
Performs various computational tasks and measures execution time.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time
import math


class PythonBenchmarkNode(Node):
    """Python benchmark node that performs computational tasks."""

    def __init__(self):
        super().__init__('python_benchmark_node')
        self.publisher_ = self.create_publisher(Float64, 'python_benchmark_result', 10)
        self.timer = self.create_timer(1.0, self.run_benchmark)
        self.get_logger().info('Python benchmark node started')

    def fibonacci(self, n):
        """Calculate Fibonacci number recursively."""
        if n <= 1:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    def matrix_multiply(self, size):
        """Perform matrix multiplication."""
        a = [[i * j for j in range(size)] for i in range(size)]
        b = [[i + j for j in range(size)] for i in range(size)]
        result = [[0 for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    result[i][j] += a[i][k] * b[k][j]
        
        return result

    def numerical_computation(self):
        """Perform numerical computations."""
        total = 0.0
        for i in range(1000000):
            total += math.sin(i) * math.cos(i)
        return total

    def run_benchmark(self):
        """Run benchmark tests and publish results."""
        results = {}

        # Fibonacci benchmark
        start_time = time.perf_counter()
        fib_result = self.fibonacci(30)
        fib_time = time.perf_counter() - start_time
        results['fibonacci'] = fib_time
        self.get_logger().info(f'Fibonacci(30) took {fib_time:.6f} seconds')

        # Matrix multiplication benchmark
        start_time = time.perf_counter()
        matrix_result = self.matrix_multiply(100)
        matrix_time = time.perf_counter() - start_time
        results['matrix_multiply'] = matrix_time
        self.get_logger().info(f'Matrix multiplication (100x100) took {matrix_time:.6f} seconds')

        # Numerical computation benchmark
        start_time = time.perf_counter()
        num_result = self.numerical_computation()
        num_time = time.perf_counter() - start_time
        results['numerical'] = num_time
        self.get_logger().info(f'Numerical computation took {num_time:.6f} seconds')

        # Publish total time
        total_time = fib_time + matrix_time + num_time
        msg = Float64()
        msg.data = total_time
        self.publisher_.publish(msg)
        self.get_logger().info(f'Total benchmark time: {total_time:.6f} seconds')


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
