# dofbot_telemetry_cpp

## Descripción General

`dofbot_telemetry_cpp` es un paquete ROS2 en C++ especializado en la **gestión y transmisión de telemetría del robot DOFBot** en tiempo real. Este paquete actúa como un sistema de monitoreo que permite leer, validar y transmitir el estado operativo y espacial del robot sin interrumpir los procesos de control.

El DOFBot es un manipulador robótico de 6 grados de libertad (6 DOF) con gripper. Este paquete coordina la supervisión de sus parámetros de movimiento para garantizar un seguimiento seguro y preciso.

---

## Estructura del Paquete

```text
dofbot_telemetry_cpp/
├── README.md                    # Documentación del paquete
├── package.xml                  # Metadatos ROS2 y dependencias
├── CMakeLists.txt               # Configuración de compilación (ament_cmake)
├── LICENSE                      # Licencia MIT
│
└── src/
    ├── telemetry.cpp            # Nodo publicador de telemetría
    └── telemetry_subs.cpp       # Nodo suscriptor para monitoreo
```
---

## Archivos Principales

### 1. **src/telemetry.cpp** - Nodo Publicador
Nodo ROS2 que implementa:

- **Inicialización de un publicador en el tópico /telemetry_cpp.**

- **Ejecución cíclica mediante temporizador (Wall Timer) a 1 Hz.**

- **Empaquetado de variables espaciales y de estado utilizando la interfaz personalizada** dofbot_interfaces::msg::Telemetry.

**Importancia:** Actúa como el transmisor central del estado del robot, asegurando que el resto de la red robótica conozca la posición y la fase operativa en todo momento.
### 2. **src/telemetry_subs.cpp** - Nodo Suscriptor


Nodo ROS2 que implementa:

**Suscripción:** activa al tópico /telemetry_cpp con una profundidad de cola (QoS) de 10 mensajes.

**Función de retroalimentación (callback) asíncrona.**

**Registro visual en terminal mediante macros de logging RCLCPP_INFO.**

**Importancia:** Permite validar el flujo de información y monitorear la telemetría en tiempo real, facilitando los procesos de depuración (debugging) y validación de control.
## Cómo Usar

### Instalación

cd ~/ROS2Dev/ws_scara
colcon build --packages-select dofbot_telemetry_cpp
source install/setup.bash

### Ejecutar

# Terminal 1: Ejecutar el publicador (Transmisor)
ros2 run dofbot_telemetry_cpp telemetry_node_pub

# Terminal 2: Ejecutar el suscriptor (Monitor)
ros2 run dofbot_telemetry_cpp telemetry_node_sub

## Datos Monitoreados
El paquete actualmente transmite y valida las siguientes variables de estado:

**status:** Fase operativa del sistema robótico (ej: "STAND BY").

**pos_x:** Coordenada espacial actual en el eje X.

**pos_y:** Coordenada espacial actual en el eje Y.

**pos_z:** Coordenada espacial actual en el eje Z.

## Referencias
ROS2 C++ Publisher and Subscriber

ROS2 Custom Interfaces

**Licencia:** MIT | **Mantenedor:** Felipe Rivas (rivascf@gmail.com)