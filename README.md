# Smart India Hackathon 2025
## Team Genesis – Gas Detection and Mapping in Underground Mines using Autonomous Drone

### Project Overview
This repository features a fully autonomous drone designed to operate in GPS-denied environments for hazardous gas detection and underground mine mapping.
The system leverages LiDAR 360 and the Optical Flow Sensor (PMW3901) for navigation and obstacle avoidance, ensuring safe and reliable operations in complex underground terrains.

### Key Features
- Autonomous navigation in GPS-denied environments.
- Gas detection and mapping in underground mines.
- Advanced sensors for obstacle detection and environment mapping.
- LoRa mesh communication using Breadcrumb Repeater Modules.
- MATLAB Simulink + Stateflow simulation for path planning and control logic.
- Optional support for ROS + Gazebo simulation in Ubuntu.

###  Sensors Used
- PMW3901 Optical Flow Sensor → Object detection and navigation.
- Bosch BNO055 IMU → Acceleration and gyroscopic measurements.
- MQ-9 Sensor → Detection of CO and CH₄ gases.
- SCD-40 NDIR Sensor → Detection of CO₂ gas.
- AO-O2 Sensor → Oxygen level monitoring.
- 360° LiDAR → 3D mapping and obstacle avoidance.

### Communication System – Breadcrumb Repeater
- The drone communicates using a LoRa-based mesh network:
- Each Breadcrumb Repeater consists of:
-- STM32F401CCU6 microcontroller
-- LoRa Radio module
-- Independent LiPo power source
-- A signal strength threshold (in dBm) is set based on terrain conditions.
-- When the drone’s signal drops below the threshold, it deploys a breadcrumb repeater as a payload.
-- These repeaters form a LoRa mesh network, relaying data back to the base station.
-- Self-healing network → even if one repeater fails, data transmission continues via alternative routes.

### Simulation and Path Planning
- MATLAB Simulink + Stateflow used to simulate drone behavior.
- Integrated sensors (MQ-9, NDIR, AO-O2, LiDAR) in signal processing blocks for data acquisition.
- Path Planning Algorithm includes:
- Takeoff
- Forward / Left / Right movement
- Obstacle avoidance
- Return and landing
- Scope blocks used for visualizing sensor outputs.
- Alternative simulation possible with MATLAB Simulink + Gazebo + ROS in Ubuntu for higher fidelity.
