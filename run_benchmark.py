#!/usr/bin/env python3
"""
Main benchmark script for ROS2 language performance evaluation.

This script acts as the 'pinger' and controller. It launches a 'pong' node
(written in C++, Python, or Rust), sends it a message, and waits for the
message to be echoed back, measuring the round-trip latency.

It iterates through a list of predefined targets (different languages) and
prints a comparative summary at the end.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
import time
import subprocess
import sys
import numpy as np
import collections

from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header

# --- Benchmark Target Configuration ---
# Defines the different language nodes to be benchmarked.
# The 'executable' is what `ros2 run <package> <executable>` expects.
TARGETS = [
    {
        'lang': 'Python',
        'package': 'ros2_lang_eval',
        'executable': 'python_benchmark_node.py',
        'pong_topic': 'pong_python',
    },
    {
        'lang': 'C++',
        'package': 'ros2_lang_eval',
        'executable': 'cpp_benchmark_node',
        'pong_topic': 'pong_cpp',
    },
    {
        'lang': 'Rust',
        'package': 'ros2_lang_eval_rust',
        'executable': 'rust_benchmark_node',
        'pong_topic': 'pong_rust',
    },
]

class BenchmarkRunner(Node):
    """Node for running the benchmark, sending pings and receiving pongs."""

    def __init__(self, pong_topic):
        super().__init__('benchmark_runner')
        self.pong_received_time = None
        self.pong_received = False

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.publisher = self.create_publisher(PointCloud2, 'ping', qos_profile)
        self.subscription = self.create_subscription(
            PointCloud2,
            pong_topic,
            self.pong_callback,
            qos_profile)
        
    def pong_callback(self, msg):
        self.pong_received_time = self.get_clock().now()
        self.pong_received = True

    def create_point_cloud_message(self, num_points=100000):
        points = np.random.rand(num_points, 3).astype(np.float32)
        msg = PointCloud2()
        msg.header = Header(stamp=self.get_clock().now().to_msg(), frame_id='benchmark_frame')
        msg.height = 1
        msg.width = num_points
        msg.is_dense = True
        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]
        msg.point_step = 12
        msg.row_step = msg.point_step * num_points
        msg.data = points.tobytes()
        msg.is_bigendian = sys.byteorder != 'little'
        return msg

    def run_single_test(self, message):
        self.pong_received = False
        self.pong_received_time = None
        
        self.publisher.publish(message)
        
        timeout_sec = 5.0
        start_wait_time = time.monotonic()
        while not self.pong_received and (time.monotonic() - start_wait_time) < timeout_sec:
            rclpy.spin_once(self, timeout_sec=0.01)

        if not self.pong_received:
            return None

        msg_timestamp = rclpy.time.Time.from_msg(message.header.stamp)
        latency_ns = self.pong_received_time.nanoseconds - msg_timestamp.nanoseconds
        return latency_ns / 1e6  # Convert to milliseconds

def run_benchmark_for_target(target, num_iterations, num_points):
    """Launches and benchmarks a single target language node."""
    print(f"\n--- Benchmarking {target['lang']} ---")
    
    node_cmd = ['ros2', 'run', target['package'], target['executable']]
    pong_process = subprocess.Popen(node_cmd)
    print(f"Launched '{' '.join(node_cmd)}'. Waiting for initialization...")
    time.sleep(5)

    runner = BenchmarkRunner(target['pong_topic'])
    latencies = []
    
    try:
        message = runner.create_point_cloud_message(num_points)
        
        print("Running warm-up iterations...")
        for _ in range(5):
            runner.run_single_test(message)
            time.sleep(0.1)

        print("Starting benchmark...")
        for i in range(num_iterations):
            latency_ms = runner.run_single_test(message)
            if latency_ms is not None:
                latencies.append(latency_ms)
                print(f"Iteration {i+1}/{num_iterations}: Latency = {latency_ms:.3f} ms")
            else:
                print(f"Iteration {i+1}/{num_iterations}: Failed (Timeout)")
            time.sleep(0.1)
    finally:
        print("Shutting down node...")
        pong_process.terminate()
        pong_process.wait()
        runner.destroy_node()

    if not latencies:
        return None
    
    return {
        'avg': np.mean(latencies),
        'std': np.std(latencies),
        'min': np.min(latencies),
        'max': np.max(latencies),
    }

def main(args=None):
    rclpy.init(args=args)
    
    num_iterations = 20
    num_points = 100000
    all_results = collections.OrderedDict()

    print("====== ROS2 Language Performance Benchmark ======")
    print(f"Message Type: PointCloud2 ({num_points} points)")
    print(f"Iterations per target: {num_iterations}")
    print("===============================================")
    
    for target in TARGETS:
        results = run_benchmark_for_target(target, num_iterations, num_points)
        if results:
            all_results[target['lang']] = results
        else:
            print(f"!!! Benchmark for {target['lang']} failed. Skipping. !!!")

    rclpy.shutdown()

    print("\n\n--- Benchmark Summary ---")
    if all_results:
        header = f"{'{'Language'}':<10} | $'{'Avg Latency (ms)'}':<20} | $'{'Std Dev (ms)'}':<15} | $'{'Min (ms)'}':<10} | $'{'Max (ms)'}':<10}"
        print(header)
        print('-' * len(header))
        for lang, results in all_results.items():
            print(f"{lang:<10} | {results['avg']:<20.3f} | {results['std']:<15.3f} | {results['min']:<10.3f} | {results['max']:<10.3f}")
    else:
        print("No results recorded. All benchmarks may have failed.")
    print('-' * len(header))


if __name__ == '__main__':
    main()
