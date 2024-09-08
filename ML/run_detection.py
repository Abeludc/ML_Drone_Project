import cv2
import argparse
from edge_tpu_silva import process_detection

def run_detection(save_output=False):
    model_path = '/home/pi/Desktop/ML/models/edgetpu_models/640_visdrone_yolo8n_edgetpu.tflite'
    video_path = 'short_video.mp4'

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Configurar VideoWriter si se requiere guardar el video
    if save_output:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('/home/pi/Desktop/ML/proc_video_8n640.mp4', fourcc, fps, (frame_width, frame_height))

    # Procesar la detección
    results = process_detection(
        model_path=model_path,
        input_path=video_path,
        imgsz=640,
        threshold=0.5,
        verbose=True,
        show=False,  # Esto habilita la visualización sin procesamiento adicional
    )

    try:
        for objs_lst, fps in results:
            if save_output:
                ret, frame = cap.read()
                if not ret:
                    break

                # Dibujar detecciones en el cuadro y guardarlo
                for obj in objs_lst:
                    bbox = obj['bbox']
                    label = obj['label']
                    conf = obj['conf']
                    color = (0, 255, 0)  # Color estático por simplicidad

                    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
                    cv2.putText(frame, f'{label} {conf:.2f}', (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                out.write(frame)
            else:
                # Simplemente procesar cuadros sin guardarlos
                cap.grab()  # Capturar cuadros sin decodificar si no se guarda para reducir la carga
    finally:
        cap.release()
        if save_output:
            out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run object detection and optionally save the output video with annotations.')
    parser.add_argument('--save', action='store_true', help='Save the video output')
    args = parser.parse_args()

    run_detection(save_output=args.save)
