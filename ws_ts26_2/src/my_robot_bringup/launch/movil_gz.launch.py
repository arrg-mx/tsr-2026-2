import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    pkg_my_robot_description = get_package_share_directory('my_robot_description')
    pkg_my_robot_bringup = get_package_share_directory('my_robot_bringup')

    urdf_path = os.path.join(pkg_my_robot_description, 'urdf', 'my_robot.urdf.xacro')
    gazebo_config_path = os.path.join(pkg_my_robot_bringup, 'config', 'gazebo_bridge.yaml')
    rviz_path = os.path.join(pkg_my_robot_description, 'rviz', 'my_robot_config.rviz')
    
    # --- CAMBIO AQUÍ: Nombre del archivo del mundo ---
    world_path = os.path.join(pkg_my_robot_bringup, 'worlds', 'world_config.world')
    
    use_sim_time = {'use_sim_time': True}

    robot_description_content = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_content}, use_sim_time]
    )

    gz_ros_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': gazebo_config_path}, use_sim_time],
        output='screen'
    )

    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path, '--render-engine', 'ogre'],
        output='screen'
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'mobile_robot',
            # --- CAMBIO AQUÍ: Debe coincidir con <world name="..."> dentro de world_config.world ---
            '-world', 'world_config' 
        ],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_path],
        parameters=[use_sim_time]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gz_sim,
        spawn_entity,
        gz_ros_bridge_node,
        rviz_node
    ])