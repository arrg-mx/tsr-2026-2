 # File: ROS2 Jazzy on NVIDIA Jetson Nano

#---------- Stage 1: Builder ------------
# 1. Toma como base una imagne ya existente para crear la
# nueva imagen
FROM dustynv/ros:jazzy-ros-base-r36.4.0-cu128-24.04

# Solucion a la migracion de llaves de ROS2 
# Issue: https://discourse.openrobotics.org/t/ros-signing-key-migration-guide/43937/30
# jetson-sontainers issue solved: 
# https://github.com/dusty-nv/jetson-containers/issues/1124    
RUN curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 2. Instalar las librerias de construccion necesarias a nivel
# Sistema Operativo (Ubuntu/linux)
RUN apt-get update && \
    apt-get install python3-pip python3-dev python3-smbus python3-smbus2 python3-pil i2c-tools -y && \
    apt install ros-jazzy-rmw-cyclonedds-cpp -y && \
    rm -rf /var/lib/apt/list/*
    
# Copiamos el archivo de requerimientos (python)
# al directorio temporal de linux /tmp/    
# COPY requirements.txt /tmp/requirements.txt

# Instalamos las dependencias del archivo de 
# requerimientos (python) a nivel global
# RUN pip3 install --no-cache-dir -r requirements.txt

# COPY docker/entrypoint.sh /entrypoint.sh

# RUN sudo chmod +x /entrypoint.sh

#---------- Stage 2: Runtime ------------
# Agregamos un usuario local y le asignamos permisos
# de super usuario para no usar root
#RUN useradd -ms /bin/bash robot && \
#    usermod -aG sudo robot

# Cambiamos la ejecución al usuario dofbotx
# Recomendable (opcional)
# USER robot
USER ubuntu
# WORKDIR /home/dofbotx
# Asignamos el directorio de trabajo del usuario
# dofbotx
# WORKDIR /home/robot 
WORKDIR /home/ubuntu 

# Copiamos el archivo bash_aliases al directorio 
# del contenedor /home/ubuntu/.bash_aliases
# COPY bash_aliases /home/robot/.bash_aliases
COPY bash_aliases /home/ubuntu/.bash_aliases

# Agregamos dos variables de entorno en el contenedor
ENV ROS_DOMAIN_ID=10
#ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# ENV DEV_MODE=true

# Comando por default
# ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
