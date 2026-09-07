import cv2
import insightface
from insightface.app import FaceAnalysis
 
# Initialize with lightweight model for CPU
app = FaceAnalysis(name="buffalo_s", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(320, 320))
 
# Open webcam
cap = cv2.VideoCapture(0)
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
    faces = app.get(frame)
    for face in faces:
        box = face.bbox.astype(int)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        embedding = face.embedding   # this is your 512-D vector
        print("Embedding shape:", embedding.shape)
 
    cv2.imshow("Face Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()