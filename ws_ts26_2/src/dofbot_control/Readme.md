<div align="center">

# `dofbot_control`
**Temas Selectos de Robótica · UNAM Facultad de Ingeniería**

</div>

---

## ¿Qué hace este paquete?

Implementa un **Action Server** que recibe comandos para mover el gripper del brazo Dofbot. A diferencia de un servicio normal, este patrón permite:

- Validar la meta **antes** de ejecutarla
- Reportar **progreso en tiempo real** (feedback)
- Retornar un **resultado final** con éxito o falla

> **¿Por qué una Acción y no un Servicio?**  
> Un servicio bloquea al cliente hasta que termina, sin saber qué pasa en medio. Una acción es para tareas largas (como mover un motor durante 3 segundos) donde necesitas saber cómo va el movimiento.

---

## Árbol de archivos

```
dofbot_control/
├── dofbot_control/
│   ├── __init__.py
│   └── DofbotSimpleActionServer.py   → lógica completa del Action Server
├── resource/
│   └── dofbot_control
├── setup.py                          → registra el ejecutable simple_actionserver
├── package.xml                       → tipo de build: ament_python, licencia MIT
└── README.md
```

---

## Ejecutar el nodo

```bash
ros2 run dofbot_control simple_actionserver
```

El entry point `simple_actionserver` está definido en `setup.py` y apunta a la función `init_action_srv()` del archivo principal.

---

## `DofbotSimpleActionServer.py`

Este es el único archivo de lógica del paquete. Se divide en cuatro etapas claras:

---

### Etapa 1 — Crear el Action Server

```python
self._action_srv = ActionServer(
    self,
    GripperCmd,
    'gripper_command',
    self.__execute_callback
)
```

Al inicializar el nodo se registra el Action Server sobre el tópico `gripper_command`.  
Cuando llegue una meta, ROS 2 llamará automáticamente a `__execute_callback`.

---

### Etapa 2 — Validar la meta recibida

```python
def __validate_range(self, value, min_val, max_val, strict=False):
```

Antes de mover cualquier cosa, se validan **dos reglas**:

| Parámetro | Rango válido | Si falla... |
|---|---|---|
| `gripper_state` | Entre `OPEN (-1.4209)` y `CLOSE (0.0)` | `goal_handle.abort()` |
| `duration` | Entre `0.0` y `10.0` segundos | `goal_handle.abort()` |

>  Si cualquiera de las dos falla, el servidor llama `abort()`, retorna un `Result` con `success=False` y **no ejecuta nada**. Esto protege al hardware de comandos fuera de rango.

El parámetro `strict=True` cambia `<` por `<=` para incluir o excluir los extremos del rango según se necesite.

---

### Etapa 3 — Ejecutar con feedback

```python
delta = (goal_state - igripper_state) / int(goal_duration)
start_time = time.time()

while int(time.time() - start_time) < int(goal_duration):
    feedback_msg = GripperCmd.Feedback()
    feedback_msg.current_state = igripper_state
    igripper_state += delta
    goal_handle.publish_feedback(feedback_msg)
    time.sleep(1.0)
```

**¿Qué hace este loop?**

1. Calcula cuánto debe avanzar el gripper **por segundo** (`delta`)
2. Cada segundo publica el estado actual como `Feedback` para que el cliente lo vea en tiempo real
3. Incrementa el estado simulado y espera 1 segundo antes del siguiente ciclo

>  **Nota importante:** el valor `igripper_state = -0.7045` es una posición inicial **simulada** (indicado con el comentario `# Just for fun`). En un robot real, este valor se leería del sensor del servo.

---

### Etapa 4 — Retornar el resultado

```python
goal_handle.succeed()
result = GripperCmd.Result()
result.current_state = goal_state
result.success = True
result.string_status_message = "Gripper move successfully."
return result
```

Al salir del loop, se llama `succeed()` para indicar que la tarea terminó correctamente y se retorna el `Result` con el estado final del gripper.

---

### Función de entrada `init_action_srv()`

```python
def init_action_srv(args=None):
    rclpy.init(args=args)
    simple_actionserver = DofbotSimpleActionSrv('gripper_action_srv_node')
    try:
        rclpy.spin(simple_actionserver)
    except KeyboardInterrupt:
        ...
    finally:
        rclpy.shutdown()
```

Es el **punto de entrada** del ejecutable. Inicializa ROS 2, crea el nodo y lo mantiene vivo con `spin()`. Si el usuario presiona `Ctrl+C`, captura la señal y apaga el nodo limpiamente.

---

## Flujo completo resumido

```
Cliente envía Goal
       │
       ▼
  ¿gripper_state en rango? ──No──► abort() + Result(success=False)
       │ Sí
       ▼
  ¿duration en rango?      ──No──► abort() + Result(success=False)
       │ Sí
       ▼
  Loop por N segundos
  ├── publica Feedback cada segundo
  └── incrementa estado simulado
       │
       ▼
  succeed() + Result(success=True)
```

---

## Tipos de mensaje utilizados

Todos definidos en el paquete `dofbot_interfaces`:

| Tipo | Campo clave | Descripción |
|---|---|---|
| `GripperCmd.Goal` | `gripper_state`, `duration` | Meta enviada por el cliente |
| `GripperCmd.Feedback` | `current_state` | Estado del gripper en tiempo real |
| `GripperCmd.Result` | `success`, `current_state`, `string_status_message` | Resultado final |

---

## Probar desde terminal

```bash
# En una terminal: levantar el servidor
ros2 run dofbot_control simple_actionserver

# En otra terminal: enviar una meta manualmente
ros2 action send_goal /gripper_command \
  dofbot_interfaces/action/GripperCmd \
  "{gripper_state: -1.4209, duration: 3.0}"
```
