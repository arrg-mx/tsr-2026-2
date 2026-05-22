#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# Importamos la libreria para ActionServer
from rclpy.action import ActionServer
# Importamos la libreria personalizada de mensajes (ActionMessage)
from dofbot_interfaces.action import GripperCmd
import math
import time

class DofbotSimpleActionSrv(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

        # Crear el ActionServer
        self._action_srv = ActionServer(
            self,
            GripperCmd,
            'gripper_command',
            self.__execute_callback
        )
        self.get_logger().info(f"Dofbot ActionServer {node_name} inicializado.")

    def __validate_range(self, value, min_val, max_val, strict=False):
        if strict:
            if value <= min_val or value >= max_val:
                False
        else:        
            if value < min_val or value > max_val:
                return False
            
        return True    

    def __execute_callback(self, goal_handle):
        # Regibimos una nueva meta del tipo GripperCmd.Goal
        self.get_logger().info(f"   Reibimos una nueva GOAL")
        # 1. Recuperamos los datos de la meta
        goal_state = goal_handle.request.gripper_state
        goal_duration = goal_handle.request.duration

        # 2. Evaluamos si la meta es vaida
        # Si no cumple con los parámetros se rechaza
        if (self.__validate_range(goal_state, GripperCmd.Goal.OPEN, GripperCmd.Goal.CLOSE)):
            goal_handle.abort()
            result = GripperCmd.Result()
            result.success = False
            result.string_status_message = f"ERROR: GRIPPER_STATE {goal_state} debe estar entre {GripperCmd.Goal.CLOSE} y {GripperCmd.Goal.OPEN}."
            result.current_state = 0.0
            return result
        if (self.__validate_range(goal_duration, 0.0, 10.0) ):
            goal_handle.abort()
            result = GripperCmd.Result()
            result.success = False
            result.string_status_message = f"ERROR: DURATION {goal_state} debe estar entre {0.0} y {10.0}."
            result.current_state = 0.0
            return result
        # 3. Acondicionamos los datos de execusion
        # en caso de ser necesario
        # --------- Just for this demo -------
        # Si el gripper fuera real entonces se lee el valor actual del gripper
        igripper_state = -0.7045 # Just for fun
        delta = (igripper_state - goal_state) / int(goal_duration)
        start_time = time.time()
        while (time.time() - start_time) < goal_duration:
            feedback_msg = GripperCmd.Feedback()
            feedback_msg.current_state = igripper_state + delta
            goal_handle.publish_feedback(feedback_msg)

        # 3. Terminamos la ejecusion de manera exitosa
        goal_handle.succeed()
        result = GripperCmd.Result()
        result.current_state = goal_state
        result.success = True
        result.string_status_message = "Gripper move succesfully."
        return result

        
def init_action_srv(args=None):
    pass

if __name__ == "__main__":
    init_action_srv()