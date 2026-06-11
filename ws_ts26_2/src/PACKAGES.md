# Descripción de Paquetes – Dofbot ROS 2

Cada paquete tiene una responsabilidad única y bien definida. Aquí se describe qué hace cada uno y su árbol de archivos.

---

## 1. `dofbot_interfaces` — Mensajes personalizados

**¿Qué hace?**  
Define los tipos de datos propios del proyecto: mensajes (`.msg`), servicios (`.srv`) y acciones (`.action`). Todos los demás paquetes dependen de este.

**Tipo de build:** `ament_cmake`

```
dofbot_interfaces/
├── msg/
│   └── Telemetry.msg          # status, pos_x, pos_y, pos_z
├── srv/
│   └── GetStatus.srv          # Request: is_robot_active | Response: is_active, success, message
├── action/
│   └── GripperCmd.action      # Goal: gripper_state, duration | Result: success | Feedback: current_state
├── CMakeLists.txt             # Registra los archivos con rosidl_generate_interfaces
└── package.xml
```

>  **Clave:** Sin este paquete, ningún otro puede compilar. Siempre compílalo primero.

---

## 2. `dofbot_config` — Servidor de parámetros

**¿Qué hace?**  
Levanta un nodo ROS 2 que actúa como almacén centralizado de parámetros del robot (nombre, IP, joints, velocidades). Valida los valores antes de aceptarlos.

**Tipo de build:** `ament_python`

```
dofbot_config/
├── dofbot_config/
│   ├── __init__.py
│   └── parameter_server.py    # Nodo DofbotParamSrv: declara y valida parámetros
├── config/
│   ├── dofbot_params.yaml     # Parámetros por defecto (YAML)
│   └── dofbot_arm_config.yaml # Configuración de grupos de joints
├── launch/
│   └── param_srv.launch.py    # Lee ROBOT_NAME e IPADDR del entorno y lanza el nodo
├── setup.py
└── package.xml
```

>  **Clave:** Usa `add_on_set_parameters_callback` para rechazar IPs inválidas o periodos negativos antes de que se apliquen.

---

## 3. `dofbot_control` — Control del gripper (Action Server)

**¿Qué hace?**  
Implementa un Action Server que recibe comandos de posición para el gripper, valida los rangos, ejecuta el movimiento de forma incremental y publica feedback en tiempo real.

**Tipo de build:** `ament_python`

```
dofbot_control/
├── dofbot_control/
│   ├── __init__.py
│   └── DofbotSimpleActionServer.py  # Nodo ActionServer: valida, ejecuta y da feedback
├── setup.py                         # Entry point: simple_actionserver
└── package.xml
```

>  **Clave:** El pattern Goal → Feedback → Result es el núcleo de ROS 2 Actions. El nodo valida que `gripper_state` esté en rango `[OPEN, CLOSE]` y que `duration` sea `[0, 10]` segundos antes de ejecutar.

---

## 4. `dofbot_services` — Servicios ROS 2

**¿Qué hace?**  
Ejemplo de patrón cliente-servidor en ROS 2. El servidor responde si el robot está activo; el cliente hace la petición y espera la respuesta.

**Tipo de build:** `ament_python`

```
dofbot_services/
├── dofbot_services/
│   ├── __init__.py
│   ├── dofbot_server.py    # Nodo servidor: responde GetStatus con is_active y success
│   └── dofbot_client.py    # Nodo cliente: llama al servicio con reintentos (3 intentos)
├── setup.py                # Entry points: status_srv, status_client
└── package.xml
```

>  **Clave:** El cliente usa `wait_for_service()` con timeout para no bloquearse indefinidamente. Implementa un contador de reintentos antes de rendirse.

---

## 5. `dofbot_telemetry` — Telemetría del sistema (Python)

**¿Qué hace?**  
Publica periódicamente el estado del sistema (CPU, RAM, disco, red, ROS) como mensajes `DiagnosticArray`. También incluye soporte para Jetson mediante `jtop`.

**Tipo de build:** `ament_python`

```
dofbot_telemetry/
├── dofbot_telemetry/
│   ├── Telemetry.py           # Publicador simple: publica posición en /telemetry
│   ├── TelemetrySubs.py       # Suscriptor simple: escucha /telemetry
│   ├── robot_telem.py         # Nodo principal: publica DiagnosticArray con SysInfo
│   ├── jtop_telem.py          # Nodo Jetson: publica diagnósticos vía jtop
│   └── telem_utils/
│       ├── sysinfo.py         # Clase SysInfo (CPU, RAM, disco, red, ROS)
│       └── jtop_utils.py      # Funciones para convertir datos de jtop a DiagnosticStatus
├── setup.py                   # Entry points: telemetry, telem_sub, robot_telem, jtop_telem
└── package.xml                # Depende de dofbot_interfaces y diagnostic_msgs
```

>  **Clave:** `robot_telem.py` usa `_find_key_recursive()` para extraer campos del reporte de `SysInfo` de forma segura, sin importar si alguna clave falta.

---

## 6. `dofbot_telemetry_cpp` — Telemetría en C++

**¿Qué hace?**  
Versión en C++ del publicador y suscriptor de telemetría. Útil para comparar el patrón pub/sub entre Python y C++.

**Tipo de build:** `ament_cmake`

```
dofbot_telemetry_cpp/
├── src/
│   ├── telemetry.cpp       # Publicador: publica en /telemetry_cpp cada 1 segundo
│   └── telemetry_subs.cpp  # Suscriptor: escucha /telemetry_cpp e imprime en logger
├── CMakeLists.txt          # Compila dos ejecutables: telemetry_node_pub y telemetry_node_sub
└── package.xml
```

>  **Clave:** En C++ el timer usa `std::chrono_literals` (`1s`). El binding del callback se hace con `std::bind`.

---

## 7. `ts26_2_description` — Descripción URDF del robot

**¿Qué hace?**  
Define el modelo visual, de colisión e inercial del robot completo (base móvil + brazo) en formato Xacro para ser usado en RViz y Gazebo.

**Tipo de build:** `ament_cmake`

```
ts26_2_description/
├── urdf/
│   ├── common_properties.xacro  # Materiales y macros de inercia (box, cylinder, sphere)
│   ├── arm.xacro                # Links y joints del brazo (arm_base, forearm, hand)
│   ├── arm_ig.xacro             # Plugins Gazebo para el brazo (PID controller)
│   ├── mobile_ig.xacro          # Plugins Gazebo para base móvil (DiffDrive)
│   └── mobile.urdf              # URDF plano de la base (versión simplificada)
├── launch/
│   └── mobile.launch.xml        # Lanza robot_state_publisher + RViz
└── rviz/
    └── urdf_config.rviz         # Configuración de visualización en RViz
```

>  **Clave:** Xacro permite usar propiedades (`${wheel_radius}`) y macros reutilizables para no repetir código de inercia en cada link.

---

## 8. `arrg_utils` — Librería de utilidades del sistema

**¿Qué hace?**  
Librería Python independiente de ROS que recopila información del sistema: CPU, RAM, disco, red y entorno ROS. Usada por `dofbot_telemetry`.

```
arrg_utils/
├── arrg_utils/
│   ├── __init__.py     # Exporta SysInfo
│   └── sysinfo.py      # Clase SysInfo con get_system_report() y get_system_snapshot()
├── samples/            # Ejemplos de salida JSON en distintas plataformas
├── setup.py
└── README.md
```

**Métodos principales de `SysInfo`:**

| Método | Retorna |
|---|---|
| `get_system_report()` | Dict completo: host, CPU, RAM, disco, red, ROS |
| `get_system_snapshot()` | Dict resumido: cpu%, RAM, disco, IP, hora |
| `get_cpu_usage()` | Lista de stats por núcleo |
| `get_free_ram()` | total, used, free, available (GB) |
| `get_free_disk()` | size, used, available (GB) |
| `get_ros_info()` | versión, distro, domain_id |

---

## Resumen de dependencias

```
arrg_utils (sin dependencias ROS)
    ↑
dofbot_interfaces (base de todos)
    ↑
    ├── dofbot_telemetry  ←── arrg_utils
    ├── dofbot_telemetry_cpp
    ├── dofbot_services
    └── dofbot_control

dofbot_config (independiente, solo rclpy)
ts26_2_description (sin deps de runtime)
```
