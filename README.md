# Raspberry Pi Pico Projects

A collection of my Raspberry Pi Pico and Pico W projects using MicroPython, including sensors, robotics, Wi-Fi, and embedded systems.

## About

This repository contains my Raspberry Pi Pico projects created using MicroPython and Arduino Lab for MicroPython. It is used to track my progress, experiment with microcontrollers, and build projects using sensors, motors, and other hardware components.

## Folder Structure

```text
pi-pico-projects/
│
├── basics/              # Basic MicroPython and hardware experiments
├── communication/       # Wi-Fi, Bluetooth, RF, and wireless projects
├── data-handling/       # CSV files, logging, and file processing
├── modules/             # Reusable custom MicroPython modules
├── robots/              # Robot projects using motors, chassis, and sensors
├── sensors/             # Individual sensor readings and tests
└── README.md
```

## Topics Covered

- MicroPython programming
- GPIO control
- Sensors
- PWM
- ADC
- Displays
- Motor control
- Robotics
- Wi-Fi communication
- IoT projects
- Embedded systems

## Hardware

- Raspberry Pi Pico
- Raspberry Pi Pico W
- Sensors
- Motors
- Motor driver boards
- Robot chassis
- LCD displays
- Servo motors
- Other electronic components

## Tools

- Language: MicroPython
- IDE: Arduino Lab for MicroPython
- Editor: Visual Studio Code / Arduino Lab for MicroPython
- Hardware Platform: Raspberry Pi Pico / Pico W

## Goals

- Improve embedded programming skills
- Learn MicroPython
- Build projects using sensors and motors
- Create more advanced robotics systems
- Explore IoT and wireless communication

## How to Run

### General Setup

1. Install MicroPython on the Raspberry Pi Pico.
2. Upload the required `.py` files to the Pico.
3. Upload any required custom modules from the `modules/` folder.
4. Run the main program.

### Wi-Fi Controlled Robots

For Wi-Fi robot projects:

1. Upload the robot code and required modules.
2. Connect the Raspberry Pi Pico W to Wi-Fi.
3. Open the control webpage in a browser.
4. Enter robot's IP Address.
5. Use the controls to send commands to the robot.

Control Interface:
- [Wi-Fi Robot Dashboard](https://moonpreneurcode.github.io/WiFi-Controlled-Robot-Dashboard-2/)

### Bluetooth Controlled Robots

For Bluetooth robot projects:

1. Upload the robot code and required modules.
2. Connect to robot using Bluetooth.
3. Open the control interface.
4. Use the controls to send commands to the robot.

Control Interface:
- [Bluetooth Robot Dashboard](https://moonpreneurcode.github.io/BLE-Controlled-Robot-Dashboard-3/)

## Notes

* The hardware connections used in these projects can be changed to fit your setup.
* You do not necessarily need to use the exact same pins, sensors, modules, or other hardware shown in the code.
* If you change the hardware configuration, update the corresponding pins and settings in the code.
* Custom modules in the `modules/` folder can also be modified or replaced with compatible implementations when needed.

## Progress

This repository will continue to grow as I build more Raspberry Pi Pico projects, explore new sensors and communication methods, and develop increasingly complex embedded systems and robotics projects.


