#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
# importamos la libreria de mensajes
# de ROS2 diagnistic_msgs: KeyValue, DiagnosticArray
from diagnostic_msgs.msg import KeyValue, DiagnosticStatus, DiagnosticArray
# importamos la(s) librerias externas
from .telem_utils.sysinfo import SysInfo

class DofbotTelemNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # definimos el publicador
        self.__diag_pub = self.create_publisher(
            DiagnosticArray, 
            "/diagnostics",
            10
        )
        self._diag_arr = DiagnosticArray()
        self.__telem_report = SysInfo()
        self.__diag_timer = self.create_timer(5.0, self._on_diag_timer)

        self.get_logger().info(f"{node_name} inicializado...")

    def _find_key_recursive(self, data, target_key):
        """
        Busca una clave de forma recursiva dentro de diccionarios o listas anidadas.
        Devuelve el valor si lo encuentra, o None si no existe.
        """
        if isinstance(data, dict):
            if target_key in data:
                return data[target_key]
            for key, value in data.items():
                result = self._find_key_recursive(value, target_key)
                if result is not None:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = self._find_key_recursive(item, target_key)
                if result is not None:
                    return result
        return None


    def _on_diag_timer(self):
        # 0. Obtencion del reporte de arrg_utils.sysinfo
        # raw_report = si.get_system_report()
        raw_report = self.__telem_report.get_system_report()
        # 1. Extraemos las secciones con la función de búsqueda
        cpu_stats = self._find_key_recursive(raw_report, 'cpu_stats')
        disk = self._find_key_recursive(raw_report, 'disk')
        ram = self._find_key_recursive(raw_report, 'ram')
        ip = self._find_key_recursive(raw_report, 'ip')
        ros = self._find_key_recursive(raw_report, 'ros')
        # 2. Ajustamos el contenedor del mensaje de ROS 2
        # DiagnosticsArray
        self._diag_arr.header.stamp = self.get_clock().now().to_msg()
        status_list = []

        # 3. Procesamos las secciones del reporte y las incluimos en el mensaje
        # formato de salida
        if isinstance(cpu_stats, list):
            for core in cpu_stats:
                if isinstance(core, dict) and core.get('type') == 'core':
                    label = core.get('label', 'Unknown_Core')
                    usage = core.get('usage')

                    if usage is not None:
                        cpu_status = DiagnosticStatus()
                        cpu_status.level = DiagnosticStatus.OK
                        cpu_status.name = f"cpu_core_{label}"
                        cpu_status.message = f"Métricas por núcleo del CPU({label})"
                        cpu_status.hardware_id = f"{label}"
                        cpu_status.values.append(KeyValue(
                            key='usage',
                            value=str(usage)
                        ))

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