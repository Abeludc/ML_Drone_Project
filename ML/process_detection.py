def process_detection(model_path, input_path, imgsz, threshold, verbose, show):
    # Logic to load the model and process the video frame by frame
    # Inference will be performed using the YOLO model optimized for Edge TPU
    # Returns a generator that produces lists of detected objects and fps per frame

    # Example implementation (this should be adapted to your specific logic)
    results = []
    for frame in video_frames:
        # Detection inference
        detected_objects = infer(frame, model_path, imgsz, threshold)
        results.append((detected_objects, fps))
        if verbose:
            print(f"Detected: {len(detected_objects)} objects at {fps} FPS")
    
    return results

