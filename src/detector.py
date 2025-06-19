from ultralytics import YOLO
import cv2

class PeopleDetector:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")
    
    def detect(self, frame):
        results = self.model.predict(frame, verbose=False)
        # print(f"Results: {results}")
        result = results[0]
        # print(f"Result: {result}")
        boxes = result.boxes
        # print(f"Boxes: {boxes}")
        people_boxes = []

        for box in boxes:
            # print(f"Box: {box}")
            cls = int(box.cls[0])
            if cls == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                people_boxes.append((x1, y1, x2, y2))

        return people_boxes

# TESTES
if __name__ == "__main__":
    frame = cv2.imread("sample/image.png")
    
    detector = PeopleDetector()
    
    boxes = detector.detect(frame)
    
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Teste Detectar Pessoas", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()