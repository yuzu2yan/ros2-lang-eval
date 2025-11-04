#!/usr/bin/env python3
"""
Benchmark runner script that runs all three language implementations
and collects performance metrics.
"""

import subprocess
import signal
import sys
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class BenchmarkSubscriber(Node):
    """Subscriber to collect benchmark results."""

    def __init__(self, language_name):
        super().__init__(f'benchmark_subscriber_{language_name}')
        self.language_name = language_name
        self.results = []
        self.subscription = self.create_subscription(
            Float64,
            f'{language_name}_benchmark_result',
            self.callback,
            10)

    def callback(self, msg):
        """Callback to receive benchmark results."""
        self.results.append(msg.data)
        self.get_logger().info(
            f'{self.language_name} benchmark result: {msg.data:.6f} seconds')


def run_benchmark(language_name, duration=10):
    """Run a benchmark node for a specified duration."""
    rclpy.init()
    
    subscriber = BenchmarkSubscriber(language_name)
    
    # Start the benchmark node
    if language_name == 'python':
        process = subprocess.Popen(
            ['ros2', 'run', 'ros2_lang_eval', 'python_benchmark_node'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    elif language_name == 'cpp':
        process = subprocess.Popen(
            ['ros2', 'run', 'ros2_lang_eval', 'cpp_benchmark_node'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    elif language_name == 'rust':
        # Note: Rust node needs to be built separately
        process = subprocess.Popen(
            ['cargo', 'run', '--release', '--manifest-path', 'src/rust/Cargo.toml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    else:
        print(f'Unknown language: {language_name}')
        return None

    # Run for specified duration
    start_time = time.time()
    while time.time() - start_time < duration:
        rclpy.spin_once(subscriber, timeout_sec=0.1)
        time.sleep(0.1)

    # Stop the process
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

    subscriber.destroy_node()
    rclpy.shutdown()

    # Calculate average
    if subscriber.results:
        avg_time = sum(subscriber.results) / len(subscriber.results)
        return {
            'language': language_name,
            'average_time': avg_time,
            'results': subscriber.results
        }
    return None


def main():
    """Run benchmarks for all languages."""
    print("ROS2 Language Performance Comparison")
    print("=" * 50)
    
    languages = ['python', 'cpp', 'rust']
    all_results = {}

    for lang in languages:
        print(f"\nRunning {lang} benchmark...")
        try:
            result = run_benchmark(lang, duration=10)
            if result:
                all_results[lang] = result
                print(f"{lang} average: {result['average_time']:.6f} seconds")
        except Exception as e:
            print(f"Error running {lang} benchmark: {e}")

    # Print summary
    print("\n" + "=" * 50)
    print("Benchmark Summary")
    print("=" * 50)
    
    if all_results:
        # Sort by average time
        sorted_results = sorted(
            all_results.items(),
            key=lambda x: x[1]['average_time'])
        
        for lang, result in sorted_results:
            print(f"{lang:10s}: {result['average_time']:.6f} seconds")
        
        # Calculate speedup
        if len(sorted_results) > 1:
            baseline = sorted_results[0][1]['average_time']
            print("\nSpeedup compared to fastest:")
            for lang, result in sorted_results:
                speedup = result['average_time'] / baseline
                print(f"{lang:10s}: {speedup:.2f}x")


if __name__ == '__main__':
    main()
