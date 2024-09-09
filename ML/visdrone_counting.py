import cv2
import argparse
from edge_tpu_silva import process_detection

def run_detection(target_label='car', save_output=False):
    model_path = '/home/pi/Desktop/ML/models/edgetpu_models/640_visdrone_yolo8s_edgetpu.tflite'
    video_path = 'people1.mp4'
    object_count = 0
    min_distance = 100  # Minimum distance to consider two detections as the same object
    detection_history = []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Setup VideoWriter only if saving is required
    if save_output:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('/home/pi/Desktop/ML/processed_video_cars.mp4', fourcc, fps, (frame_width, frame_height))

    # Process detection
    results = process_detection(
        model_path=model_path,
        input_path=video_path,
        imgsz=640,
        threshold=0.5,
        verbose=True,
        show=False,  # This enables visual display without additional processing
    )

    try:
        for objs_lst, fps in results:
            current_detections = []

            if save_output:
                ret, frame = cap.read()
                if not ret:
                    break

            for obj in objs_lst:
                if obj['label'] == target_label:
                    bbox = obj['bbox']
                    cx = (bbox[0] + bbox[2]) / 2  # Calculate the center x-coordinate
                    cy = (bbox[1] + bbox[3]) / 2  # Calculate the center y-coordinate
                    current_detections.append((cx, cy))

            # Avoid double counting by comparing current detections with a history of last detections
            for detection in current_detections:
                if not any(
                    [
                        abs(detection[0] - hist_det[0]) < min_distance and abs(detection[1] - hist_det[1]) < min_distance
                        for hist_lst in detection_history for hist_det in hist_lst
                    ]
                ):
                    object_count += 1

            detection_history.append(current_detections)
            # Keep the history limited to avoid memory issues
            if len(detection_history) > 10:
                detection_history.pop(0)

            print(f"Total {target_label}s detected: {object_count}")

            if save_output:
                # Show the count on the video
                cv2.putText(frame, f'{target_label.capitalize()} Count: {object_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                for obj in objs_lst:
                    if obj['label'] == target_label:
                        bbox = obj['bbox']
                        label = obj['label']
                        conf = obj['conf']
                        color = (0, 255, 0)  # Static color for simplicity

                        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
                        cv2.putText(frame, f'{label} {conf:.2f}', (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                out.write(frame)
            else:
                cap.grab()  # Grab frames without decoding if not saving to reduce overhead
    finally:
        cap.release()
        if save_output:
            out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run object detection and optionally save the output video with annotations.')
    parser.add_argument('--save', action='store_true', help='Save the video output')
    parser.add_argument('--target', type=str, default='car', help='Object to detect and count (default: car)')
    args = parser.parse_args()

    run_detection(target_label=args.target, save_output=args.save)

