# dofbot_interfaces

Paquete ROS 2 que define las interfaces de comunicación personalizadas para el robot **Dofbot**. Incluye mensajes (`msg`), servicios (`srv`) y acciones (`action`) utilizados por los demás paquetes del workspace `ws_ts26_2`.

- **Versión:** 0.0.0
- **Mantenedor:** 
- **Licencia:** MIT
- **Tipo de build:** `ament_cmake`

---

## Contenido

- [Estructura del paquete](#estructura-del-paquete)
- [Dependencias](#dependencias)
- [Compilación e instalación](#compilación-e-instalación)
- [Interfaces definidas](#interfaces-definidas)
  - [Mensaje: Telemetry.msg](#mensaje-telemetrymsg)
  - [Servicio: GetStatus.srv](#servicio-getstatussrv)
  - [Acción: GripperCmd.action](#acción-grippercmdaction)
- [Uso desde otros paquetes](#uso-desde-otros-paquetes)
- [Licencia](#licencia)

---

## Estructura del paquete

```
dofbot_interfaces/
├── action/
│   └── GripperCmd.action       # Definición de la acción para controlar el gripper
├── msg/
│   └── Telemetry.msg           # Mensaje de telemetría del robot
├── srv/
│   └── GetStatus.srv           # Servicio para consultar el estado del robot
├── CMakeLists.txt              # Configuración de compilación con ament_cmake
├── package.xml                 # Metadatos y dependencias del paquete
└── LICENSE                     # Licencia MIT
```

---

## Dependencias

| Dependencia | Tipo | Descripción |
|---|---|---|
| `ament_cmake` | buildtool | Sistema de build de ROS 2 |
| `rosidl_default_generators` | buildtool | Generador de código para interfaces ROS 2 |
| `rosidl_default_runtime` | exec | Runtime necesario para usar las interfaces generadas |
| `ament_lint_auto` | test | Linting automático en pruebas |
| `ament_lint_common` | test | Reglas de linting comunes de ROS 2 |

---

## Compilación e instalación

Desde la raíz del workspace (`ws_ts26_2`):

```bash
# Compilar únicamente este paquete
colcon build --packages-select dofbot_interfaces

# Cargar el entorno generado
source install/setup.bash
```

> **Nota:** Si utilizas CycloneDDS como middleware, asegúrate de tener configurada la variable de entorno antes de compilar o ejecutar:
> ```bash
> export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
> ```

---

## Interfaces definidas

### Mensaje: `Telemetry.msg`

**Archivo:** `msg/Telemetry.msg`

Mensaje para publicar información de telemetría del robot. Transporta el estado textual y la posición 3D del robot en cada instante.

#### Campos

| Campo | Tipo | Descripción |
|---|---|---|
| `status` | `string` | Estado actual del robot en formato de texto |
| `pos_x` | `float32` | Posición en el eje X (metros) |
| `pos_y` | `float32` | Posición en el eje Y (metros) |
| `pos_z` | `float32` | Posición en el eje Z (metros) |

#### Ejemplo de uso (Python)

```python
from dofbot_interfaces.msg import Telemetry

msg = Telemetry()
msg.status = "IDLE"
msg.pos_x = 0.15
msg.pos_y = 0.0
msg.pos_z = 0.30

publisher.publish(msg)
```

---

### Servicio: `GetStatus.srv`

**Archivo:** `srv/GetStatus.srv`

Servicio para consultar si el robot está activo. Un nodo cliente envía una petición al servidor y recibe una respuesta con el estado y banderas de resultado.

#### Estructura

```
# --- REQUEST ---
bool is_robot_active       # Indica si se desea consultar un robot activo

---

# --- RESPONSE ---
bool is_active             # Estado actual del robot (activo / inactivo)
bool success               # Bandera de éxito del proceso
string string_status_message  # Mensaje descriptivo del resultado
```

#### Campos de la petición (Request)

| Campo | Tipo | Descripción |
|---|---|---|
| `is_robot_active` | `bool` | Parámetro de consulta: `true` para verificar robot activo |

#### Campos de la respuesta (Response)

| Campo | Tipo | Descripción |
|---|---|---|
| `is_active` | `bool` | `true` si el robot está activo, `false` en caso contrario |
| `success` | `bool` | `true` si el servicio se ejecutó correctamente |
| `string_status_message` | `string` | Mensaje textual con la descripción del estado |

#### Ejemplo de uso (Python)

```python
from dofbot_interfaces.srv import GetStatus

# Cliente
client = node.create_client(GetStatus, 'get_status')
request = GetStatus.Request()
request.is_robot_active = True

future = client.call_async(request)
# En el callback:
# response.is_active, response.success, response.string_status_message
```

---

### Acción: `GripperCmd.action`

**Archivo:** `action/GripperCmd.action`

Acción para controlar el gripper (pinza) del Dofbot. Sigue el patrón estándar de ROS 2 Actions con tres secciones: **Goal** (meta), **Result** (resultado) y **Feedback** (retroalimentación durante la ejecución).

#### Estructura completa

```
# --- GOAL ---
float32 OPEN  = -1.4209   # Constante: valor de apertura del gripper
float32 CLOSE =  0.0      # Constante: valor de cierre del gripper

float32 gripper_state     # Estado objetivo del gripper
float32 duration          # Tiempo de ejecución de la tarea (segundos)

---

# --- RESULT ---
float32 current_state         # Valor final del gripper al terminar
bool success                  # Bandera de éxito del proceso
string string_status_message  # Mensaje descriptivo del resultado

---

# --- FEEDBACK ---
float32 current_state         # Valor intermedio del gripper durante la ejecución
```

#### Constantes predefinidas

| Constante | Valor | Descripción |
|---|---|---|
| `OPEN` | `-1.4209` | Posición de apertura completa del gripper |
| `CLOSE` | `0.0` | Posición de cierre completo del gripper |

#### Campos del Goal

| Campo | Tipo | Descripción |
|---|---|---|
| `gripper_state` | `float32` | Posición objetivo del gripper. Usar `OPEN` o `CLOSE` u otro valor dentro del rango |
| `duration` | `float32` | Tiempo en segundos para completar el movimiento |

#### Campos del Result

| Campo | Tipo | Descripción |
|---|---|---|
| `current_state` | `float32` | Posición final del gripper al concluir la acción |
| `success` | `bool` | `true` si la acción se completó exitosamente |
| `string_status_message` | `string` | Mensaje descriptivo del resultado final |

#### Campos del Feedback

| Campo | Tipo | Descripción |
|---|---|---|
| `current_state` | `float32` | Posición actual del gripper durante la ejecución (publicada periódicamente) |

#### Ejemplo de uso (Python)

```python
from dofbot_interfaces.action import GripperCmd

# Enviar una meta al Action Server
goal = GripperCmd.Goal()
goal.gripper_state = GripperCmd.Goal.OPEN  # -1.4209
goal.duration = 2.0  # segundos

send_goal_future = action_client.send_goal_async(
    goal,
    feedback_callback=feedback_callback
)

# En el feedback_callback:
def feedback_callback(feedback_msg):
    current = feedback_msg.feedback.current_state
    print(f"Estado actual del gripper: {current}")
```

---

## Uso desde otros paquetes

Para utilizar las interfaces de `dofbot_interfaces` en otro paquete del workspace, agrega las siguientes dependencias en su `package.xml`:

```xml
<depend>dofbot_interfaces</depend>
```

Y en su `CMakeLists.txt` (paquetes C++):

```cmake
find_package(dofbot_interfaces REQUIRED)
```

En Python, las interfaces se importan directamente tras compilar el workspace:

```python
from dofbot_interfaces.msg import Telemetry
from dofbot_interfaces.srv import GetStatus
from dofbot_interfaces.action import GripperCmd
```

---

## Licencia

Este paquete está distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
