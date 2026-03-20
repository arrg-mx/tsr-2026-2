cmake_minimum_required(VERSION 3.8)
project(dofbot_telemetry_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(dofbot_interfaces REQUIRED)

# Agrega os puntos de acceso para ejecutar los programas
# Compilacion/construccion
add_executable(telemetry_node_pub src/telemetry.cpp)
ament_target_dependencies(telemetry_node_pub rclcpp dofbot_interfaces)
# punto de acceso del subscriptor
add_executable(telemetry_node_sub src/telemetry_subs.cpp)
ament_target_dependencies(telemetry_node_sub rclcpp dofbot_interfaces)


# Asigna la salida del resultado de la construccion a la
# carpeta de ejecusion
install(TARGETS
  telemetry_node_pub
  telemetry_node_sub
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
