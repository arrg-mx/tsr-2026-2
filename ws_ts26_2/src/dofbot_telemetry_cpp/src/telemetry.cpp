
#include "dofbot_interfaces/msg/telemetry.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class TelemetryPub : public rclcpp::Node {
public:
  TelemetryPub() : Node("telemetry_node") {
    publisher_ = create_publisher<dofbot_interfaces::msg::Telemetry>(
        "/telemetry_cpp", 10);
    timer_ = create_wall_timer(
        1s, std::bind(&TelemetryPub::callback_telemetry, this));

    RCLCPP_INFO(get_logger(), "Nodo inicializado.");
  }

  void callback_telemetry() {
    auto telemetry_msg = dofbot_interfaces::msg::Telemetry();
    telemetry_msg.status = "STAND BY";
    telemetry_msg.pos_x = 0.0;
    telemetry_msg.pos_y = 0.0;
    telemetry_msg.pos_z = 0.0;

    publisher_->publish(telemetry_msg);
  }

private:
  rclcpp::Publisher<dofbot_interfaces::msg::Telemetry>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  auto telemetry_node = std::make_shared<TelemetryPub>();
  rclcpp::spin(telemetry_node);

  rclcpp::shutdown();

  return 0;
}
