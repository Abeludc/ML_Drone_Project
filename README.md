# ML Drone Project

Welcome to the ML Drone Project repository! This project focuses on autonomous drone missions using a Pixhawk flight controller and a Raspberry Pi, alongside Machine Learning (ML) implementations for object detection using YOLO and Google Coral. The repository is organized into two main sections: `Missions` and `ML`.

## Table of Contents

- [Missions](#missions)
  - [Overview](#overview)
  - [Scripts](#scripts)
- [ML](#ml)
  - [Overview](#overview-1)
  - [Scripts](#scripts-1)
  - [Media](#media)
- [Setup](#setup)
- [References](#references)

## Missions

### Overview

The `Missions` directory contains Python scripts responsible for managing and executing autonomous missions on the drone. The scripts handle tasks such as connecting to the flight controller, loading and executing waypoints, capturing video during flights, and ensuring safety measures are in place.

### Scripts

- **[`main.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/Missions/main.py):** Coordinates the entire mission execution, from connection to the Pixhawk to mission completion and safe return.
- **[`conexion_config.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/Missions/conexion_config.py):** Manages the connection between the Raspberry Pi and the Pixhawk, as well as configuring flight speed.
- **[`mission_management.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/Missions/mission_management.py):** Handles reading waypoints from files and uploading them to the Pixhawk.
- **[`mission_execution.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/Missions/mission_execution.py):** Manages the autonomous flight, including takeoff, following waypoints, and executing return-to-launch (RTL) based on various conditions.
- **[`video_capture.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/Missions/video_capture.py):** Captures video during the flight, useful for post-mission analysis.

## ML

### Overview

The `ML` directory includes scripts for running object detection using a YOLO model optimized for the Google Coral. These scripts process video footage captured by the drone, identifying objects in real-time.

### Scripts

- **[`run_detection.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/ML/run_detection.py):** Executes the object detection process on a given video, with an option to save the output video with annotated detections.
- **[`process_detection.py`](https://github.com/Abeludc/ML_Drone_Project/blob/main/ML/process_detection.py):** Handles the inference process, utilizing a YOLO model optimized for Edge TPU to detect objects frame by frame.

### Media

The `media` directory contains example outputs from the object detection process:

- **[`processed_video_8n640.mp4`](https://github.com/Abeludc/ML_Drone_Project/blob/main/ML/media/processed_video_8n640.mp4):** A video processed by the `run_detection.py` script, showcasing object detection annotations overlaid on the footage captured by the drone.

## Setup

To set up this project on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abeludc/ML_Drone_Project.git
   cd ML_Drone_Project
   ```

2. **Install dependencies:**
   Ensure that you have Python 3.7+ and the necessary libraries installed. You can install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install `edge-tpu-silva`:**
   This project uses the `edge-tpu-silva` repository for processing object detection on Google Coral. Clone and install the necessary dependencies:
   ```bash
   git clone https://github.com/DAVIDNYARKO123/edge-tpu-silva.git
   cd edge-tpu-silva
   pip install -r requirements.txt
   ```

4. **Run the Mission Scripts:**
   Navigate to the `Missions` directory and execute the main mission script:
   ```bash
   cd Missions
   python main.py --connect /dev/ttyACM0 --waypoints mymission.waypoints
   ```

5. **Run the Object Detection:**
   Navigate to the `ML` directory and execute the `run_detection.py` script to process a video:
   ```bash
   cd ML
   python run_detection.py --save
   ```

## References

- [Pixhawk Documentation](https://docs.px4.io/)
- [DroneKit-Python](http://python.dronekit.io/)
- [YOLOv4: Optimal Speed and Accuracy of Object Detection](https://arxiv.org/abs/2004.10934)
- [Google Coral](https://coral.ai/)
- [edge-tpu-silva Repository](https://github.com/DAVIDNYARKO123/edge-tpu-silva)

Feel free to explore and contribute to this project by submitting issues or pull requests. Enjoy flying and coding!
