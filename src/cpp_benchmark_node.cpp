#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64.hpp>
#include <chrono>
#include <cmath>
#include <vector>

class CppBenchmarkNode : public rclcpp::Node
{
public:
  CppBenchmarkNode() : Node("cpp_benchmark_node")
  {
    publisher_ = this->create_publisher<std_msgs::msg::Float64>("cpp_benchmark_result", 10);
    timer_ = this->create_wall_timer(
      std::chrono::seconds(1),
      std::bind(&CppBenchmarkNode::run_benchmark, this));
    RCLCPP_INFO(this->get_logger(), "C++ benchmark node started");
  }

private:
  // Recursive Fibonacci calculation
  int64_t fibonacci(int n)
  {
    if (n <= 1) {
      return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
  }

  // Matrix multiplication
  std::vector<std::vector<double>> matrix_multiply(int size)
  {
    std::vector<std::vector<double>> a(size, std::vector<double>(size));
    std::vector<std::vector<double>> b(size, std::vector<double>(size));
    std::vector<std::vector<double>> result(size, std::vector<double>(size, 0.0));

    // Initialize matrices
    for (int i = 0; i < size; ++i) {
      for (int j = 0; j < size; ++j) {
        a[i][j] = i * j;
        b[i][j] = i + j;
      }
    }

    // Perform multiplication
    for (int i = 0; i < size; ++i) {
      for (int j = 0; j < size; ++j) {
        for (int k = 0; k < size; ++k) {
          result[i][j] += a[i][k] * b[k][j];
        }
      }
    }

    return result;
  }

  // Numerical computation
  double numerical_computation()
  {
    double total = 0.0;
    for (int i = 0; i < 1000000; ++i) {
      total += std::sin(i) * std::cos(i);
    }
    return total;
  }

  void run_benchmark()
  {
    auto start = std::chrono::high_resolution_clock::now();

    // Fibonacci benchmark
    start = std::chrono::high_resolution_clock::now();
    int64_t fib_result = fibonacci(30);
    auto fib_time = std::chrono::high_resolution_clock::now() - start;
    double fib_seconds = std::chrono::duration<double>(fib_time).count();
    RCLCPP_INFO(this->get_logger(), "Fibonacci(30) took %.6f seconds", fib_seconds);

    // Matrix multiplication benchmark
    start = std::chrono::high_resolution_clock::now();
    auto matrix_result = matrix_multiply(100);
    auto matrix_time = std::chrono::high_resolution_clock::now() - start;
    double matrix_seconds = std::chrono::duration<double>(matrix_time).count();
    RCLCPP_INFO(this->get_logger(), "Matrix multiplication (100x100) took %.6f seconds", matrix_seconds);

    // Numerical computation benchmark
    start = std::chrono::high_resolution_clock::now();
    double num_result = numerical_computation();
    auto num_time = std::chrono::high_resolution_clock::now() - start;
    double num_seconds = std::chrono::duration<double>(num_time).count();
    RCLCPP_INFO(this->get_logger(), "Numerical computation took %.6f seconds", num_seconds);

    // Publish total time
    double total_time = fib_seconds + matrix_seconds + num_seconds;
    std_msgs::msg::Float64 msg;
    msg.data = total_time;
    publisher_->publish(msg);
    RCLCPP_INFO(this->get_logger(), "Total benchmark time: %.6f seconds", total_time);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CppBenchmarkNode>());
  rclcpp::shutdown();
  return 0;
}
