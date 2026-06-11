UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO
FACULTAD DE INGENIERIA

Área principal : Área de las Ciencias Físico Matemáticas y de las Ingenierías
Disciplina : Ingenierías
Entidad académica: Fac. Ingeniería
Objetivo: Documentar los paquetes realizados durante el semestre durante la clase para que los alumnos que tomen la clase en futuros semestres puedan tener una idea claara de como se estructura un repositorio de Robótica en ROS2


Nombre de los docentes responsables : M.I. ERIK PEÑA MEDINA y ING. FELIPE RIVAS CAMPOS

Alumnos: 
López Cruz Marino 
Franco Ayala Carlos Alfonso
Mota Vázquez Carlos Emiliano


# Dofbot ROS 2 – Guía de Implementación

> **Repositorio:** `ws_ts26_2` — Workspace ROS 2 (Jazzy) para el brazo robótico Dofbot sobre NVIDIA Jetson.

---

## Estructura del repositorio

```
ws_ts26_2/
└── src/
    ├── dofbot_interfaces/      # Mensajes, servicios y acciones personalizados
    ├── dofbot_config/          # Servidor de parámetros (configuración del robot)
    ├── dofbot_control/         # Action Server para control del gripper
    ├── dofbot_services/        # Cliente/Servidor de servicios ROS 2
    ├── dofbot_telemetry/       # Telemetría del sistema (Python)
    ├── dofbot_telemetry_cpp/   # Telemetría del sistema (C++)
    ├── ts26_2_description/     # Descripción URDF/Xacro del robot
    ├── my_robot_description/   # Descripción del robot móvil con brazo
    └── my_robot_bringup/       # Launch files y mundos de Gazebo

arrg_utils/                     # Librería de utilidades del sistema (CPU, RAM, disco, red)
dockerimg/                      # Dockerfile y docker-compose para Jetson
```

---

##  Dependencias previas

| Herramienta | Versión |
|---|---|
| ROS 2 | Jazzy |
| Python | 3.12+ |
| CMake | 3.8+ |
| NVIDIA JetPack | r36.4.0 |

Instala las dependencias del sistema:
```bash
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
pip install arrg-utils --break-system-packages
```

---

##  Pasos para implementar

### 1. Clonar el repositorio

```bash
git clone <url-del-repo> ~/dofbotx
cd ~/dofbotx/ws_ts26_2
```

### 2. Instalar dependencias de ROS 2

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Compilar el workspace

```bash
colcon build --symlink-install
```

> `--symlink-install` permite editar archivos Python sin recompilar.

### 4. Sourcear el workspace

```bash
source install/setup.bash
# O usa el alias:
srcthis
```

### 5. Configurar variables de entorno

```bash
export ROBOT_NAME=dofbot_arm
export IPADDR=192.168.200.128
export ROS_DOMAIN_ID=10
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

---

##  Docker (Jetson)

```bash
cd dockerimg/
docker-compose up
```

El contenedor monta `/home/arrusr/dofbotx` como `/home/robot` y expone todos los dispositivos I2C/USB necesarios.

---

## Ejecutar los paquetes

### Servidor de parámetros
```bash
ros2 launch dofbot_config param_srv.launch.py
```

### Telemetría del sistema
```bash
ros2 run dofbot_telemetry robot_telem
```

### Servidor de servicios
```bash
ros2 run dofbot_services status_srv
ros2 run dofbot_services status_client
```

### Action Server del gripper
```bash
ros2 run dofbot_control simple_actionserver
```

### Telemetría Jetson (jtop)
```bash
ros2 run dofbot_telemetry jtop_telem
```

---

## Dependencias entre paquetes

```
dofbot_interfaces
    ↑
    ├── dofbot_telemetry
    ├── dofbot_telemetry_cpp
    ├── dofbot_services
    └── dofbot_control
```

> `dofbot_interfaces` debe compilarse primero. Contiene todos los tipos de mensaje personalizados.

---

## Tópicos y servicios relevantes

| Nombre | Tipo | Descripción |
|---|---|---|
| `/telemetry` | `dofbot_interfaces/Telemetry` | Posición y estado del robot |
| `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | CPU, RAM, disco, red |
| `/dofbot_status_srv` | `dofbot_interfaces/GetStatus` | Estado activo/inactivo del robot |
| `/gripper_command` | `dofbot_interfaces/GripperCmd` | Acción para mover el gripper |

---

## Alias útiles (dentro del contenedor)

```bash
srcthis     # source ./install/setup.bash
ros2path    # lista todos los paquetes en AMENT_PREFIX_PATH
```


Para cambiar a CyclonDDS library

```console
$ sudo apt install ros-${ROS_DISTRO}-rmw-cyclonedds-cpp

$ export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```
