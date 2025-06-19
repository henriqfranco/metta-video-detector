import cv2
import json
from detector import PeopleDetector
import os

class VideoProcessor:
    def __init__(self, video_path, output_path, alert_threshold):
        self.video_path = video_path
        self.output_path = output_path
        self.alert_threshold = alert_threshold
        self.detector = PeopleDetector()
        self.history = []
        self.alerts = []

    def process(self):
        os.makedirs(self.output_path, exist_ok=True)

        cap = cv2.VideoCapture(self.video_path)

        # Pega informações do vídeo original para criar a nova versão
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Processando vídeo: {total_frames} frames")

        # Usa as informações do vídeo original para criar o output
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(
            os.path.join(self.output_path, "processed_video.mp4"),
            fourcc,
            fps,
            (width, height)
        )

        frame_id = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            boxes = self.detector.detect(frame)

            for (x1, y1, x2, y2) in boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            count = len(boxes)
            self.history.append({ "id": frame_id, "count": count })

            if count >= self.alert_threshold:
                self.alerts.append({ "id": frame_id, "count": count })

            out.write(frame)

            frame_id += 1

        with open(os.path.join(self.output_path, "history.json"), "w") as f:
            json.dump(self.history, f, indent=4)

        with open(os.path.join(self.output_path, "alerts.json"), "w") as f:
            json.dump(self.alerts, f, indent=4)

        cap.release()
        out.release()

# TESTES
if __name__ == "__main__":
    processor = VideoProcessor(
        video_path="sample/people-walking.mp4",
        output_path="output_results",
        alert_threshold=3
    )
    processor.process()