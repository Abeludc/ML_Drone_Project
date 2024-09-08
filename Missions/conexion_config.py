from dronekit import connect

def connect_vehicle(connection_string):
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    return vehicle

def set_flight_speed(vehicle, speed_mps):
    print(f"Setting airspeed to {speed_mps} m/s")
    vehicle.airspeed = speed_mps
