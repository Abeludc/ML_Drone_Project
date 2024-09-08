import time
from dronekit import VehicleMode

def arm_and_takeoff(vehicle, target_altitude):
    print("Performing pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off to altitude: %s meters" % target_altitude)
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def execute_mission(vehicle, hold_waypoints=[]):
    print("Starting mission")
    vehicle.commands.next = 0
    vehicle.mode = VehicleMode("AUTO")

    while True:
        next_wp = vehicle.commands.next
        print("Distance to waypoint %s: %s meters" % (next_wp, distance_to_current_waypoint(vehicle)))

        if next_wp in hold_waypoints:
            print(f"Holding position at waypoint {next_wp} for 7 seconds...")
            time.sleep(7)

        if next_wp == vehicle.commands.count:
            print("Mission completed")
            break
        time.sleep(1)

    print("Returning to launch")
    vehicle.mode = VehicleMode("RTL")

def distance_to_current_waypoint(vehicle):
    next_waypoint = vehicle.commands.next
    if next_waypoint == 0:
        return None
    mission_item = vehicle.commands[next_waypoint - 1]
    lat = mission_item.x
    lon = mission_item.y
    alt = mission_item.z
    target_wp_location = LocationGlobalRelative(lat, lon, alt)
    return get_distance_metres(vehicle.location.global_frame, target_wp_location)

def get_distance_metres(location1, location2):
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
