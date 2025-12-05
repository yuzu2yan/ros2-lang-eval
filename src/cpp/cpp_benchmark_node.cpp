/**
 * @file cpp_benchmark_node.cpp
 * @brief ROS2 C++ node that acts as a 'pong' for latency benchmarks.
 * @details It subscribes to a 'ping' topic and immediately republishes the
 * message to a 'pong' topic. This is used to measure round-trip time.
 */

#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"

class CppBenchmarkNode : public rclcpp::Node {
public:
    CppBenchmarkNode() : Node("cpp_benchmark_node") {
        // Use a reliable QoS profile to match the pinger
        auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).reliable();

        // Create a publisher for the pong topic
        publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("pong_cpp", qos);

        // Create a subscriber to the ping topic
        subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
            "ping", qos,
            std::bind(&CppBenchmarkNode::pong_callback, this, std::placeholders::_1));
        
        RCLCPP_INFO(this->get_logger(), "C++ Pong Node for PointCloud2 benchmark started.");
    }

private:
    void pong_callback(const sensor_msgs::msg::PointCloud2::SharedPtr msg) const {
        // Receives a message and immediately republishes it.
        publisher_->publish(*msg);
    }

    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_;
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CppBenchmarkNode>());
    rclcpp::shutdown();
    return 0;
}