#!/bin/bash

set -e

source /opt/ros/jazzy/setup.bash

cd /home/robot/workspace

if [ -d "src" ]; then
    echo "Installing ROS dependencies..."
    sudo rosdep install --from-paths src --ignore-src -r -y

    BUILD_NEEDED=false

    if [ ! -d "install" ]; then
        BUILD_NEEDED=true
    fi

    if [ "$BUILD_NEEDED" = true ]; then
        echo "Building ROS2 workspace..."

        if [ "$DEV_MODE" = "true" ]; then
            colcon build --symlink-install
        else
            colcon build --merge-install
        fi
    else
        echo "Skipping build (cache detected)"
    fi
fi

if [ -f "install/setup.bash" ]; then
    source install/setup.bash
fi

exec "$@"