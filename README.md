# ROS2 Language Performance Comparison

This ROS2 package provides benchmark nodes implemented in Python, C++, and Rust to compare performance across different programming languages in ROS2 environments.

## Features

- **Python Benchmark Node**: Pure Python implementation using rclpy
- **C++ Benchmark Node**: C++ implementation using rclcpp
- **Rust Benchmark Node**: Rust implementation using rclrs

Each benchmark node performs the same computational tasks:
1. **Fibonacci Calculation**: Recursive Fibonacci(30) computation
2. **Matrix Multiplication**: 100x100 matrix multiplication
3. **Numerical Computation**: Trigonometric operations (sin/cos) on 1 million iterations

## Requirements

- ROS2 (Humble or newer)
- Python 3.8+
- C++17 compatible compiler (GCC 8+ or Clang 8+)
- Rust toolchain (for Rust benchmark)
- rclpy, rclcpp packages
- rclrs (Rust ROS2 client library)

## Building

### Python and C++

```bash
# Build the package
colcon build --packages-select ros2-lang-eval

# Source the workspace
source install/setup.bash
```

### Rust

The Rust benchmark node needs to be built separately:

```bash
cd src/rust
cargo build --release
```

## Running Individual Benchmarks

### Python

```bash
ros2 run ros2-lang-eval python_benchmark_node
```

### C++

```bash
ros2 run ros2-lang-eval cpp_benchmark_node
```

### Rust

```bash
cd src/rust
cargo run --release
```

## Running All Benchmarks

Use the provided benchmark runner script:

```bash
python3 run_benchmark.py
```

This will run all three benchmarks sequentially and display a summary comparison.

## Expected Results

Typically, you should see:
- **C++**: Fastest execution time
- **Rust**: Comparable to C++ performance
- **Python**: Slower execution time due to interpreted nature

Actual performance will vary based on:
- Hardware specifications
- Compiler optimizations
- Python interpreter version
- System load

## Topics

Each benchmark node publishes results to:
- `python_benchmark_result` (std_msgs/Float64)
- `cpp_benchmark_result` (std_msgs/Float64)
- `rust_benchmark_result` (std_msgs/Float64)

## License

MIT License
