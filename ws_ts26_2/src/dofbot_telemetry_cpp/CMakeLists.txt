cmake_minimum_required(VERSION 3.8)
project(dofbot_telemetry_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(dofbot_interfaces REQUIRED)

set(dependencies
  rclcpp
  dofbot_interfaces
)

include_directories(
  include
)

add_executable(telemetry_cpp src/telemetry.cpp)
ament_target_dependencies(telemetry_cpp ${dependencies})


install(TARGETS
  #dofbot_telemetry_cpp
  DESTINATION lib/$(PROJECT_NAME)/
)

#install (
#  DIRECTORY dofbot_telemetry_cpp
#  DESTINATION share/${PROJECT_NAME}
#)

install (
  DIRECTORY include/
  DESTINATION include
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
