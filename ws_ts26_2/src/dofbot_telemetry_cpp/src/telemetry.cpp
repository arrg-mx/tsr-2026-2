
// libreria de mensajes personalizado para cpp
#include "dofbot_interfaces/msg/telemetry.hpp"
// libreria del cliente de ROS2 para CPP
#include "rclcpp/rclcpp.hpp"

// Espacio de nombres para el control del tiempo
using namespace std::chrono_literals;

// Clase donde incrustamos el publicador
// Esta clase hereda de ROS2::Node
class TelemetryPub : public rclcpp::Node {
public:
  // Definicion del constructor
  TelemetryPub() : Node("telemetry_node") {
    // Definimos el publicador del tipo de msg dofbot_interfaces::msg::Telemetry
    publisher_ = create_publisher<dofbot_interfaces::msg::Telemetry>(
        "/telemetry_cpp", 10);
    // Definimos un ROS2 Timer para ejecutar el publicador
    timer_ = create_wall_timer(
        1s, std::bind(&TelemetryPub::callback_telemetry, this));
    // Imprime un mensaje usando el sistema de mensajes de ROS2
    RCLCPP_INFO(get_logger(), "Nodo inicializado.");
  }

private:
  // Funcion de callback para el envio de mensajes
  void callback_telemetry() {
    // Crear un nvo mensaje del tipo ...Telemetry
    auto telemetry_msg = dofbot_interfaces::msg::Telemetry();
    // Llemanos el mensaje con los valores deseados
    telemetry_msg.status = "STAND BY";
    telemetry_msg.pos_x = 0.0;
    telemetry_msg.pos_y = 0.0;
    telemetry_msg.pos_z = 0.0;
    // Invocamos el metodo publish para enviar el mensaje
    publisher_->publish(telemetry_msg);
  }

  // Definicion de metodos privados
  rclcpp::Publisher<dofbot_interfaces::msg::Telemetry>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
  // Inicializar ROS2
  rclcpp::init(argc, argv);
  // Crear una nva instancia de la clase TelemetryPub
  auto telemetry_node = std::make_shared<TelemetryPub>();
  // Mantener activo el nodo indefinidamente
  rclcpp::spin(telemetry_node);
  // Termina la ejecusion de ROS2
  rclcpp::shutdown();

  return 0;
}
