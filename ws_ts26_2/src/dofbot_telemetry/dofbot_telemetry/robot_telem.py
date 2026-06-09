#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
# importamos la libreria de mensajes
# de ROS2 diagnistic_msgs: KeyValue, DiagnosticArray
from diagnostic_msgs.msg import KeyValue, DiagnosticStatus, DiagnosticArray
# importamos la(s) librerias externas
from .telem_utils.sysinfo import SysInfo
# Importamos os para acceder a las variables de entorno
import os

class DofbotTelemNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # definimos el publicador
        self.__diag_pub = self.create_publisher(
            DiagnosticArray, 
            "/diagnostics",
            10
        )
        self.declare_parameter('interval', 0.5)  # Intervalo por DEFAULT 
        self.__robot_name = os.getenv('ROBOT_NAME', 'VIRTUAL_WKS')
        self._diag_arr = DiagnosticArray()
        self.__telem_report = SysInfo()
        self.__timer_period = self.get_parameter('interval').get_parameter_value().double_value
        self.__diag_timer = self.create_timer(self.__timer_period, self._on_diag_timer)

        self.get_logger().info(f"{node_name} inicializado: System diagnostics hast started with interval {self.__timer_period} secs.")

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
        disk_stats = self._find_key_recursive(raw_report, 'disk')
        ram_stats = self._find_key_recursive(raw_report, 'ram')
        ip = self._find_key_recursive(raw_report, 'ip')
        rosinfo = self._find_key_recursive(raw_report, 'ros')
        # 2. Ajustamos el contenedor del mensaje de ROS 2
        # DiagnosticsArray
        self._diag_arr.header.stamp = self.get_clock().now().to_msg()
        status_list = []

        # 3. Procesamos las secciones del reporte y las incluimos en el mensaje
        # formato de salida
        # 3.1. Procesar CPU Info
        if isinstance(cpu_stats, list):
            for core in cpu_stats:
                if isinstance(core, dict) and core.get('type') == 'core':
                    label = core.get('label', 'Unknown_Core')
                    usaged = core.get('usaged')

                    if usaged is not None:
                        cpu_status = DiagnosticStatus()
                        cpu_status.level = DiagnosticStatus.OK
                        cpu_status.name = f"cpu_core_{label}"
                        cpu_status.message = f"Métricas por núcleo del CPU({label})"
                        cpu_status.hardware_id = f"{label}"
                        cpu_status.values.append(KeyValue(
                            key='usaged',
                            value=str(usaged)
                        ))
                        status_list.append(cpu_status)

        # 3.2. Procesar Disk Info
        if isinstance(disk_stats, dict):
            disk_status = DiagnosticStatus()
            disk_status.name = "hardware_disk"
            disk_status.message = "System Hardware [Disk Info]: Estado de almacenamiento."
            disk_status.hardware_id = "disk_drive"
            # Forma segura para filtrar datos
            for key in ['size', 'used', 'available']:
                if key in disk_stats:
                    disk_status.values.append(
                        KeyValue(key=key, value=str(disk_stats[key]))
                    )
            if disk_status.values:
                status_list.append(disk_status)
        # 3.3. Procesar RAM Info
        if isinstance(ram_stats, dict):
            ram_status = DiagnosticStatus()
            ram_status.name = "hardware_ram"
            ram_status.message = "System Hardware [RAM Info]: Estado de la memoria del sistema."
            ram_status.hardware_id = "memory_rame"
            # Forma segura para filtrar datos
            for key in ['used', 'free', 'available']:
                if key in ram_stats:
                    ram_status.values.append(KeyValue(
                        key=key,
                        value=str(ram_stats[key])
                    ))
            if ram_status.values:
                status_list.append(ram_status)
        # 3.4. Diraccion IP
        if ip is not None:
            ip_status = DiagnosticStatus()
            ip_status.name = "network_interface"
            ip_status.message = "System Hardware [IP Address]: Direccion IP activa."
            ip_status.hardware_id = "ip_address"
            ip_status.values.append(KeyValue(key='ip', value=str(ip)))
            status_list.append(ip_status)
        # 3.5. Procesar ROS Info
        if isinstance(rosinfo, dict):
            robotsys_status = DiagnosticStatus()
            robotsys_status.name = "robot_system"
            robotsys_status.message = "Robot System: Datos de asigancion del robot."
            robotsys_status.hardware_id = "robot_system"
            # Obtener los campos que necesito
            for key in ['version', 'distro', 'domain_id']:
                if key in rosinfo:
                    robotsys_status.values.append(KeyValue(
                        key=key,
                        value=str(rosinfo[key])
                    ))

            if robotsys_status.values:
                # Para acceder al nombre del robot a través de  su 
                # variable de entorno
                robotsys_status.values.append(KeyValue(
                    key='robot_name',
                    value=self.__robot_name
                ))
                status_list.append(robotsys_status)
        # 4. Asignar los estados recolectados al arreglo y publicar
        self._diag_arr.status = status_list
        self.__diag_pub.publish(self._diag_arr)



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