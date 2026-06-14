<div align="center">

# 🤖 Dofbot ROS 2 — Workspace `ws_ts26_2`

**Universidad Nacional Autónoma de México**  
**Facultad de Ingeniería**

| | |
|---|---|
| **Materia** | Temas Selectos de Robótica |
| **Área** | Ciencias Físico Matemáticas y de las Ingenierías |
| **Docentes** | M.I. Erik Peña Medina · Ing. Felipe Rivas Campos |
| **Alumnos** | López Cruz Marino · Franco Ayala Carlos Alfonso · Mota Vázquez Carlos Emiliano |

</div>

---

## ¿Qué es este repositorio?

Workspace de ROS 2 (Jazzy) para programar y controlar el brazo robótico **Dofbot** sobre una tarjeta **NVIDIA Jetson**. Cada paquete dentro de `src/` tiene su propio `README.md` con la explicación de sus archivos.

---

## Estructura general

```
ws_ts26_2/
└── src/
    ├── dofbot_interfaces/       → Tipos de datos: mensajes, servicios y acciones
    ├── dofbot_config/           → Parámetros centralizados del robot
    ├── dofbot_control/          → Mueve el gripper (Action Server)
    ├── dofbot_services/         → Comunicación petición-respuesta (Servicios)
    ├── dofbot_telemetry/        → Estado del sistema en Python
    ├── dofbot_telemetry_cpp/    → Estado del sistema en C++
    ├── ts26_2_description/      → Modelo 3D del robot (URDF/Xacro)
    ├── my_robot_description/    → Robot móvil + brazo
    └── my_robot_bringup/        → Launch files y mundos Gazebo

arrg_utils/                      → Librería Python: CPU, RAM, disco, red
dockerimg/                       → Contenedor Docker para Jetson
```

> 📌 **Regla de dependencias:** `dofbot_interfaces` debe compilarse **primero** porque todos los demás paquetes usan sus tipos de mensaje.

---

## Dependencias previas

| Herramienta | Versión |
|---|---|
| ROS 2 | Jazzy |
| Python | 3.12+ |
| CMake | 3.8+ |
| NVIDIA JetPack | r36.4.0 |

```bash
# Middleware de comunicación (más eficiente que el default)
sudo apt install ros-jazzy-rmw-cyclonedds-cpp

# Librería de utilidades del sistema
pip install arrg-utils --break-system-packages
```

---

## Pasos de implementación

### 1 · Clonar el repositorio

```bash
git clone <url-del-repo> ~/dofbotx
cd ~/dofbotx/ws_ts26_2
```

### 2 · Instalar dependencias de ROS 2

```bash
rosdep install --from-paths src --ignore-src -r -y
```

> `rosdep` lee los `package.xml` de cada paquete y descarga lo que falta automáticamente.

### 3 · Compilar

```bash
colcon build --symlink-install
```

> `--symlink-install` crea enlaces simbólicos en vez de copiar archivos. Así puedes editar código Python **sin recompilar**.

### 4 · Sourcear el workspace

```bash
source install/setup.bash
# Alias rápido dentro del contenedor:
srcthis
```

> Este paso le dice al sistema dónde están tus paquetes. Si abres una terminal nueva, debes repetirlo.

### 5 · Variables de entorno

```bash
export ROBOT_NAME=dofbot_arm
export IPADDR=192.168.200.128
export ROS_DOMAIN_ID=10
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

> `ROS_DOMAIN_ID` aísla tu red ROS 2 del resto. Si varias personas trabajan en la misma red, usan diferentes IDs.

---

## Alternativa: Docker

```bash
cd dockerimg/
docker-compose up
```

El contenedor monta tu código en `/home/robot` y expone los dispositivos I2C y USB del Jetson automáticamente. Útil para no contaminar el sistema operativo base.

---

## Ejecutar cada paquete

```bash
# Parámetros del robot
ros2 launch dofbot_config param_srv.launch.py

# Telemetría del sistema (Python)
ros2 run dofbot_telemetry robot_telem

# Servicios: servidor y cliente (en terminales separadas)
ros2 run dofbot_services status_srv
ros2 run dofbot_services status_client

# Control del gripper
ros2 run dofbot_control simple_actionserver

# Telemetría Jetson (requiere hardware físico)
ros2 run dofbot_telemetry jtop_telem
```

---

## Tópicos y servicios del sistema

| Nombre | Tipo | ¿Para qué sirve? |
|---|---|---|
| `/telemetry` | `dofbot_interfaces/Telemetry` | Posición XYZ y estado del robot |
| `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | CPU, RAM, disco, red |
| `/dofbot_status_srv` | `dofbot_interfaces/GetStatus` | ¿Está el robot activo? |
| `/gripper_command` | `dofbot_interfaces/GripperCmd` | Abrir/cerrar el gripper |

---

## Dependencias entre paquetes

```
dofbot_interfaces  ← compila primero
       ↑
       ├── dofbot_telemetry
       ├── dofbot_telemetry_cpp
       ├── dofbot_services
       └── dofbot_control
```

---

## READMEs por paquete

Cada paquete tiene su propia documentación detallada:

| Paquete | Descripción rápida |
|---|---|
| [`dofbot_interfaces`](src/dofbot_interfaces/README.md) | Tipos de datos personalizados |
| [`dofbot_config`](src/dofbot_config/README.md) | Servidor de parámetros |
| [`dofbot_control`](src/dofbot_control/README.md) | Action Server del gripper |
| [`dofbot_services`](src/dofbot_services/README.md) | Cliente y servidor de servicios |
| [`dofbot_telemetry`](src/dofbot_telemetry/README.md) | Telemetría en Python |
| [`dofbot_telemetry_cpp`](src/dofbot_telemetry_cpp/README.md) | Telemetría en C++ |
| [`ts26_2_description`](src/ts26_2_description/README.md) | Modelo URDF del robot |
