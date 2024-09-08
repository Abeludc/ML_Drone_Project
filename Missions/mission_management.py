from dronekit import Command

def read_waypoints_from_file(filename):
    print("Reading mission from file: %s" % filename)
    mission_list = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise ValueError("Unsupported waypoint file format")
            else:
                line_array = line.split('\t')
                ln_index = int(line_array[0])
                ln_currentwp = int(line_array[1])
                ln_frame = int(line_array[2])
                ln_command = int(line_array[3])
                ln_param1 = float(line_array[4])
                ln_param2 = float(line_array[5])
                ln_param3 = float(line_array[6])
                ln_param4 = float(line_array[7])
                ln_param5 = float(line_array[8])
                ln_param6 = float(line_array[9])
                ln_param7 = float(line_array[10])
                ln_autocontinue = int(line_array[11].strip())
                cmd = Command(0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue,
                              ln_param1, ln_param2, ln_param3, ln_param4,
                              ln_param5, ln_param6, ln_param7)
                mission_list.append(cmd)
    return mission_list

def upload_mission(vehicle, mission_list):
    print("Uploading mission to vehicle")
    cmds = vehicle.commands
    cmds.clear()
    for cmd in mission_list:
        cmds.add(cmd)
    cmds.upload()
    print("Mission uploaded successfully")
