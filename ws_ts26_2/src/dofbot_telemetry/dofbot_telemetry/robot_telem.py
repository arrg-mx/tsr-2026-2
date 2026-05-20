#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
# importamos la libreria de mensajes
# de ROS2 diagnistic_msgs: KeyValue, DiagnosticArray
from diagnostic_msgs.msg import KeyValue, DiagnosticStatus, DiagnosticArray
# importamos la(s) librerias externas
from arrg_utils.sysinfo import SysInfo as si

class DofbotTelemNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # definimos el publicador
        self.__diag_pub = self.create_publisher(
            DiagnosticArray, 
            "/diagnostics",
            10
        )

        self.__diag_timer = self.create_timer(5.0, self._on_diag_timer)

        self.get_logger().info(f"{node_name} inicializado...")

    def _on_diag_timer(self):
        response = DiagnosticArray()
        # definicion del header
        response.header.frame_id = ""
        response.header.stamp = self.get_clock().now().to_msg()
        diag_data = si.get_system_report()
        status = list(DiagnosticStatus)
        Status_item = DiagnosticStatus()
        Status_item.name = diag_data['host']
        Status_item.hardware_id = diag_data['platform']['additional_info']['pretty_name']
        Status_item.message = ""
        Status_item.level = DiagnosticStatus.OK
        valores = list(KeyValue)
        i = 0
        # Lectura de los CPUs
        for cpu_stat in diag_data['cpu_stats']:
            key_value = KeyValue()
            key_value.key = str(i)
            key_value._value = cpu_stat[str(i)]['usaged']
            valores.append(key_value)
            i +=1
        # Lectura de la RAM
        key_value = KeyValue()
        key_value.key = 'ram'
        key_value.value = diag_data['ram']['used']

        status.append(Status_item)

def init_node(args=None):
    rclpy.init(args=args)
    try:
        telem_node = DofbotTelemNode('telemetry_node')
        rclpy.spin(telem_node)
    except KeyboardInterrupt:
        telem_node.get_logger().info("Keyboard interrupt signal receive, shutting down node.")
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    init_node()