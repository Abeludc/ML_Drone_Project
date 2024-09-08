from picamera2 import Picamera2

def start_camera_recording():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (1440, 1080)})
    picam2.configure(video_config)
    picam2.start_and_record_video("mission_casa_video.h264")
    print("Recording started.")
    return picam2

def stop_camera_recording(picam2):
    picam2.stop_recording()
    print("Recording stopped.")
