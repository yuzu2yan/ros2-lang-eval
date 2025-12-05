cmake_minimum_required(VERSION 3.8)
project(ros2_lang_eval)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# Python package installation
ament_python_install_package(ros2_lang_eval
  PACKAGE_DIR src/python
)

# C++ executable
add_executable(cpp_benchmark_node src/cpp/cpp_benchmark_node.cpp)
target_include_directories(cpp_benchmark_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(cpp_benchmark_node
  rclcpp
  std_msgs
  sensor_msgs
)

# Install C++ executable
install(TARGETS
  cpp_benchmark_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python scripts
install(PROGRAMS
  src/ros2_lang_eval/python_benchmark_node.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()