# CSSE4011 - Prac 4
Alexander FitzGerald (45330874) and Desmond Gan (45264410)

### Overview

8 static nodes are to be set up in a grid (4 of which have ultrasonic capabilities). These help with tracking 2 mobile nodes, and the information is sent to a base node connected to a computer.

This project uses TagoIO as the dashboard. We sent the training data to the dashboard and used KNN to locate the nodes. 

### External libraries / products
 - `pykalman`: Kalman filter
 - `tago`: TagoIO dashboard
 - `sklearn`: KNN implementation
 - `matplotlib`: Plotting
 - `numpy`: Numerical libraries
 - `scipy`: Numerical method libraries / algorithm (used for multilateration)

### Directory structure
```
.
├── apps
│   ├── p3
│   │   ├── base
│   │   │   ├── CMakeLists.txt
│   │   │   ├── prj.conf
│   │   │   ├── README.rst
│   │   │   ├── sample.yaml
│   │   │   └── src
│   │   │       └── main.c
│   │   ├── mobile
│   │   │   ├── CMakeLists.txt
│   │   │   ├── prj.conf
│   │   │   ├── README.rst
│   │   │   ├── sample.yaml
│   │   │   └── src
│   │   │       └── main.c
│   │   ├── static_ahu
│   │   │   ├── CMakeLists.txt
│   │   │   ├── particle_argon.overlay
│   │   │   ├── prj.conf
│   │   │   ├── README.rst
│   │   │   ├── sample.yaml
│   │   │   └── src
│   │   │       └── main.c
│   │   └── static_scu
│   │       ├── CMakeLists.txt
│   │       ├── disco_l475_iot1.overlay
│   │       ├── prj.conf
│   │       ├── README.rst
│   │       ├── sample.yaml
│   │       └── src
│   │           └── main.c
├── CMakeLists.txt
├── dashboard.py
├── gui.py
├── Kconfig.csse4011
├── mlgui.py
├── myoslib
│   ├── CMakeLists.txt
│   ├── inc
│   │   ├── cli_hci.h
│   │   ├── cli_ledrgb.h
│   │   ├── cli_log.h
│   │   ├── cli_time.h
│   │   ├── hal_hci.h
│   │   ├── hal_packet.h
│   │   ├── hal_ultrasonic.h
│   │   ├── os_bluetooth.h
│   │   ├── os_hci.h
│   │   ├── os_i2c.h
│   │   ├── os_ledrgb.h
│   │   └── os_log.h
│   └── src
│       ├── cli_hci.c
│       ├── cli_ledrgb.c
│       ├── cli_log.c
│       ├── cli_time.c
│       ├── hal_hci.c
│       ├── hal_packet.c
│       ├── hal_ultrasonic.c
│       ├── os_bluetooth.c
│       ├── os_hci.c
│       ├── os_i2c.c
│       ├── os_ledrgb.c
│       ├── os_log.c
│       └── test.c
├── README.md
├── receive.py
├── serial_read.py
├── test.py
├── training.csv
├── TrainingData.xlsx
└── west.yml
```
