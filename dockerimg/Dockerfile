 # File: ROS2 Jazzy on NVIDIA Jetson Nano

#---------- Stage 1: Builder ------------
# 1. Toma como base una imagne ya existente para crear la
# nueva imagen
FROM dustynv/ros:jazzy-ros-base-r36.4.0-cu128-24.04

# 2. Instalar las librerias de construccion necesarias a nivel
# Sistema Operativo (Ubuntu/linux)
RUN apt-get update && \
    apt-get install python3-smbus i2c-tools -y && \
    rm -rf /var/lib/apt/list/*
    
# Copiamos el archivo de requerimientos (python)
# al directorio temporal de linux /tmp/    
COPY requirements.txt /tmp/requirements.txt

# Instalamos las dependencias del archivo de 
# requerimientos (python) a nivel global
RUN pip3 install --no-cache-dir -r requirements.txt

#---------- Stage 2: Runtime ------------
# Agregamos un usuario local y le asignamos permisos
# de super usuario para no usar root
RUN useradd -ms /bin/bash dofbotx && \
    usermod -aG sudo dofbotx

# Cambiamos la ejecución al usuario dofbotx
# Recomendable (opcional)
USER dofbotx
# WORKDIR /home/dofbotx
# Asignamos el directorio de trabajo del usuario
# dofbotx
WORKDIR /home/ubuntu 

# Copiamos el archivo bash_aliases al directorio 
# del contenedor /home/ubuntu/.bash_aliases
COPY bash_aliases .bash_aliases

RUN source .bash_aliases

# Agregamos dos variables de entorno en el contenedor
ENV ROS_DOMAIN_ID=10
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# Comando por default
CMD ["bash"]