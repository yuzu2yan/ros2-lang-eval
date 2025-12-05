//! ROS2 Rust node that acts as a 'pong' for latency benchmarks.
//!
//! It subscribes to a 'ping' topic and immediately republishes the message
//! to a 'pong' topic. This is used to measure round-trip time.

use rclrs::{Context, Publisher, QOS_PROFILE_DEFAULT};
use sensor_msgs::msg::PointCloud2;
use std::sync::Arc;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize ROS2
    let context = Context::new(std::env::args())?;
    let node = rclrs::create_node(&context, "rust_benchmark_node")?;

    // Create a publisher for the pong topic
    let publisher = Arc::new(node.create_publisher::<PointCloud2>("pong_rust", QOS_PROFILE_DEFAULT)?);
    
    // The callback function for the subscriber.
    // It captures a copy of the publisher Arc.
    let callback = {
        let publisher = Arc::clone(&publisher);
        move |msg: PointCloud2| {
            // Receives a message and immediately republishes it.
            // We don't care about the result of the publish call.
            let _ = publisher.publish(&msg);
        }
    };

    // Create a subscriber to the ping topic
    let _subscription = node.create_subscription::<PointCloud2, _>("ping", QOS_PROFILE_DEFAULT, callback)?;

    println!("Rust Pong Node for PointCloud2 benchmark started.");

    // Spin the node to process messages
    rclrs::spin(&node)?;

    Ok(())
}