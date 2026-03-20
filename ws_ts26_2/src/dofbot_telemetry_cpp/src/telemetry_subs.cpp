// libreria de mensajes personalizado para cpp
#include "dofbot_interfaces/msg/telemetry.hpp"
// libreria del cliente de ROS2 para CPP
#include "rclcpp/rclcpp.hpp"

using std::placeholders::_1;

class TelemetrySub : public rclcpp::Node 
{
public:
    TelemetrySub() : Node("telemetry_sub_node") {
        subscriber_ = create_subscription<dofbot_interfaces::msg::Telemetry>(
            "/telemetry_cpp", 10,
            std::bind(&TelemetrySub::on_telemetry_clbk, this, _1)
        );

        RCLCPP_INFO(get_logger(), "Nodo (subscriptor) inicializado");
    }
   
private:
    void on_telemetry_clbk(const dofbot_interfaces::msg::Telemetry &msg) const {
        RCLCPP_INFO(get_logger(), "Recibi [%s], posicion [%f, %f, %f]", 
        msg.status.c_str(), msg.pos_x, msg.pos_y, msg.pos_z);
    }

    rclcpp::Subscription<dofbot_interfaces::msg::Telemetry>::SharedPtr subscriber_;

};

int main(int argc, char **argv) {
  // Inicializar ROS2
  rclcpp::init(argc, argv);
  // Crear una nva instancia de la clase TelemetryPub
  auto telemetry_sub = std::make_shared<TelemetrySub>();
  // Mantener activo el nodo indefinidamente
  rclcpp::spin(telemetry_sub);
  // Termina la ejecusion de ROS2
  rclcpp::shutdown();

  return 0;
}