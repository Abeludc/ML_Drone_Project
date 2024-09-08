import argparse
import threading
from conexion_config import connect_vehicle, set_flight_speed
from video_capture import start_camera_recording, stop_camera_recording
from mission_management import read_waypoints_from_file, upload_mission
from mission_execution import arm_and_takeoff, execute_mission

def main():
    parser = argparse.ArgumentParser(description='Script to load and execute a mission from a .waypoints file.')
    parser.add_argument('--connect', required=True, help="Vehicle connection target string.")
    parser.add_argument('--waypoints', required=True, help="Waypoint file to load and execute.")
    parser.add_argument('--hold_wp', nargs='+', type=int, help="Waypoints where the drone should hold position for 7 seconds")

    args = parser.parse_args()

    vehicle = connect_vehicle(args.connect)

    try:
        # Start camera
        picam2 = start_camera_recording()
        time.sleep(4)

        # Read waypoints from file
        mission_list = read_waypoints_from_file(args.waypoints)

        # Upload mission to the vehicle
        upload_mission(vehicle, mission_list)

        # Arm the vehicle and take off to a safe altitude
        arm_and_takeoff(vehicle, 10)  # Adjust the altitude if needed

        # Set a fixed flight speed (e.g., 3 m/s for a slower flight)
        set_flight_speed(vehicle, 3)

        # Start monitoring threads for safety
        threading.Thread(target=monitor_keyboard_for_rtl, args=(vehicle,)).start()
        threading.Thread(target=monitor_flight_time_for_rtl, args=(vehicle,)).start()

        # Start and monitor the mission
        hold_waypoints = args.hold_wp if args.hold_wp else []
        execute_mission(vehicle, hold_waypoints)

    finally:
        print("Closing vehicle connection")
        vehicle.close()
        # Stop recording
        stop_camera_recording(picam2)

if __name__ == '__main__':
    main()
