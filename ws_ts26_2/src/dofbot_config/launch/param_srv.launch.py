# importa las librerias de acceso a las
# funciones del sistema operativo
import os
# Importa las librerias y funciones necesarias 
# para crear la accion de ros launch
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, EnvironmentVariable
from launch_ros.actions import Node

ROBOT_NAME = EnvironmentVariable('ROBOT_NAME', default_value='VIRTUAL')


def generate_launch_description():
    ld = LaunchDescription()

    param_srv_node = Node(
        package='dofbot_config',
        executable='param_srv',
        parameters=[{
            'robot_name': ROBOT_NAME
        }]
    )

    ld.add_action(param_srv_node)

    return ld


