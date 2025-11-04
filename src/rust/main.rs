use rclrs::*;
use std::time::Instant;
use std_msgs::msg::Float64;

fn fibonacci(n: u64) -> u64 {
    match n {
        0 | 1 => n,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn matrix_multiply(size: usize) -> Vec<Vec<f64>> {
    let mut a = vec![vec![0.0; size]; size];
    let mut b = vec![vec![0.0; size]; size];
    let mut result = vec![vec![0.0; size]; size];

    // Initialize matrices
    for i in 0..size {
        for j in 0..size {
            a[i][j] = (i * j) as f64;
            b[i][j] = (i + j) as f64;
        }
    }

    // Perform multiplication
    for i in 0..size {
        for j in 0..size {
            for k in 0..size {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    result
}

fn numerical_computation() -> f64 {
    let mut total = 0.0;
    for i in 0..1_000_000 {
        total += (i as f64).sin() * (i as f64).cos();
    }
    total
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let context = Context::new(std::env::args())?;
    let mut node = context.create_node("rust_benchmark_node")?;
    let publisher = node.create_publisher::<Float64>("rust_benchmark_result", 10)?;

    node.spin_once(std::time::Duration::from_millis(100));

    loop {
        // Fibonacci benchmark
        let start = Instant::now();
        let fib_result = fibonacci(30);
        let fib_duration = start.elapsed();
        println!("Fibonacci(30) took {:?} ({:.6} seconds)", fib_duration, fib_duration.as_secs_f64());

        // Matrix multiplication benchmark
        let start = Instant::now();
        let _matrix_result = matrix_multiply(100);
        let matrix_duration = start.elapsed();
        println!("Matrix multiplication (100x100) took {:?} ({:.6} seconds)", matrix_duration, matrix_duration.as_secs_f64());

        // Numerical computation benchmark
        let start = Instant::now();
        let _num_result = numerical_computation();
        let num_duration = start.elapsed();
        println!("Numerical computation took {:?} ({:.6} seconds)", num_duration, num_duration.as_secs_f64());

        // Publish total time
        let total_time = fib_duration.as_secs_f64() + matrix_duration.as_secs_f64() + num_duration.as_secs_f64();
        let mut msg = Float64::default();
        msg.data = total_time;
        publisher.publish(&msg)?;
        println!("Total benchmark time: {:.6} seconds", total_time);

        std::thread::sleep(std::time::Duration::from_secs(1));
        node.spin_once(std::time::Duration::from_millis(100));
    }
}
