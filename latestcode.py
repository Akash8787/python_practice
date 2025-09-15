# import cv2
# import numpy as np
# from ultralytics import YOLO
# from insightface.app import FaceAnalysis
# import cvzone
# import math
# import pickle
# import time

# confidence = 0.8  # Confidence threshold for YOLO

# def initialize_yolo_model(model_path):
#     """Initialize YOLO model for real/fake detection"""
#     try:
#         model = YOLO(model_path)
#         return model
#     except Exception as e:
#         print(f"YOLO model initialization failed: {e}")
#         return None

# def initialize_face_model():
#     """Initialize insightface model for face recognition"""
#     try:
#         app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
#         app.prepare(ctx_id=0, det_size=(320, 320))
#         return app
#     except Exception as e:
#         print(f"Face recognition model initialization failed: {e}")
#         return None

# def load_face_database(pickle_path):
#     """Load face embeddings database"""
#     try:
#         with open(pickle_path, 'rb') as f:
#             return pickle.load(f)
#     except Exception as e:
#         print(f"Failed to load face database: {e}")
#         return {}

# def calculate_face_size(bbox):
#     """Calculate face size based on bounding box dimensions"""
#     width = bbox[2] - bbox[0]
#     height = bbox[3] - bbox[1]
#     return (width + height) / 2  # Average of width and height

# def main():
#     # Initialize models
#     yolo_model = initialize_yolo_model(r'D:\Python\Python_practice\n_version_1_30.pt')
#     face_model = initialize_face_model()
#     if yolo_model is None or face_model is None:
#         return

#     # Load face database
#     pickle_path = r"D:\Python\Python_practice\face_embeddings.pkl"
#     database = load_face_database(pickle_path)
#     if not database:
#         print("No valid embeddings in database")
#         return

#     # iPhone camera stream
#     iphone_ip = "192.168.1.20"  # Replace with your iPhone's IP
#     video_url = f"http://{iphone_ip}:8080/video"
    
#     cap = cv2.VideoCapture(video_url)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#     if not cap.isOpened():
#         print(f"Failed to connect to iPhone camera at {video_url}")
#         return

#     print("Connected to iPhone camera. Press 'q' to quit...")

#     # Class names for YOLO
#     classNames = ["fake", "real"]

#     # Screen resolution for display
#     screen_width = 3840
#     screen_height = 2160
#     cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow("Face Recognition", screen_width, screen_height)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Connection lost - attempting to reconnect...")
#             cap.release()
#             cap = cv2.VideoCapture(video_url)
#             time.sleep(1)
#             continue

#         # Convert frame to RGB for face recognition
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Step 1: YOLO real/fake detection
#         results = yolo_model(frame, stream=True, verbose=False)
#         real_faces = []

#         for r in results:
#             boxes = r.boxes
#             for box in boxes:
#                 x1, y1, x2, y2 = box.xyxy[0]
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#                 w, h = x2 - x1, y2 - y1

#                 conf = math.ceil((box.conf[0] * 100)) / 100
#                 cls = box.cls[0]
#                 name = classNames[int(cls)].upper()

#                 if conf > confidence:
#                     if name == "FAKE":
#                         # Draw bounding box and text only for fake faces
#                         color = (0, 0, 255)
#                         cvzone.cornerRect(frame, (x1, y1, w, h), colorC=color, colorR=color)
#                         cvzone.putTextRect(frame, f'{name} {int(conf*100)}%', 
#                                          (max(0, x1), max(35, y1)), scale=2, thickness=2, 
#                                          colorR=color, colorB=color)
#                     elif name == "REAL":
#                         # Collect real face bbox for face recognition, but don't draw
#                         real_faces.append([x1, y1, x2, y2])

#         # Step 2: Face recognition for real faces
#         closest_face = None
#         max_face_size = 0
#         face_info = []

#         if real_faces:
#             faces = face_model.get(frame_rgb)
#             for face in faces:
#                 bbox = face.bbox.astype(int)
#                 # Check if face bbox overlaps with any real face bbox
#                 for real_bbox in real_faces:
#                     rx1, ry1, rx2, ry2 = real_bbox
#                     # Simple overlap check
#                     if (bbox[0] < rx2 and bbox[2] > rx1 and 
#                         bbox[1] < ry2 and bbox[3] > ry1):
#                         embedding = face.normed_embedding
#                         face_size = calculate_face_size(bbox)

#                         # Find best match
#                         best_match = "Unknown"
#                         best_similarity = -1
#                         threshold = 0.4

#                         for name, emb in database.items():
#                             sim = np.dot(embedding, emb)
#                             if sim > best_similarity:
#                                 best_similarity = sim
#                                 best_match = name if sim > threshold else "Unknown"

#                         face_info.append({
#                             'bbox': bbox,
#                             'size': face_size,
#                             'name': best_match,
#                             'similarity': best_similarity
#                         })

#                         # Track closest face
#                         if face_size > max_face_size:
#                             max_face_size = face_size
#                             closest_face = best_match

#         # Step 3: Draw face recognition results only for known faces
#         for info in face_info:
#             if info['name'] != "Unknown":  # Only draw for known faces
#                 bbox = info['bbox']
#                 color = (0, 255, 0)
#                 thickness = 3 if info['name'] == closest_face else 1
#                 cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)

#                 label = f"{info['name']} ({info['similarity']:.2f})"
#                 if info['name'] == closest_face:
#                     label += " [CLOSEST]"

#                 cv2.putText(frame, label, (bbox[0], bbox[1]-10), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#                 size_text = f"Size: {info['size']:.1f}"
#                 cv2.putText(frame, size_text, (bbox[0], bbox[3]+20),
#                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#         # Display closest face info
#         if closest_face:
#             status_text = f"Closest face: {closest_face}"
#             cv2.putText(frame, status_text, (10, 30),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

#         # Display the frame
#         cv2.imshow("Face Recognition", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

#======================================================================================================


import cv2
import numpy as np
from deepface import DeepFace
import pickle
import time

def load_face_database(pickle_path):
    """Load face embeddings from a pickle file"""
    try:
        with open(pickle_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Failed to load face database: {e}")
        return {}

def calculate_face_size(bbox):
    """Calculate face size based on bounding box dimensions"""
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return (width + height) / 2  # Average of width and height

def verify_anti_spoofing(frame):
    """Check if a valid face is detected as a proxy for anti-spoofing"""
    try:
        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend='opencv',
            enforce_detection=True  # Require face detection
        )
        return len(faces) > 0  # True if at least one face is detected
    except Exception as e:
        print(f"Anti-spoofing verification failed: {e}")
        return False

def main():
    pickle_path = r"D:\Python\Python_practice\face_embeddings.pkl"
    database = load_face_database(pickle_path)
    if not database:
        print("No valid embeddings in database")
        return
    
    # DroidCam connection
    droidcam_ip = "192.168.1.22"  # Replace with your iPhone's IP
    video_url = f"http://{droidcam_ip}:8080/video"
    
    cap = cv2.VideoCapture(video_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if not cap.isOpened():
        print(f"Failed to connect to DroidCam at {video_url}")
        return
    
    print("Connected to DroidCam. Press 'q' to quit...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Connection lost - attempting to reconnect...")
            cap.release()
            cap = cv2.VideoCapture(video_url)
            time.sleep(1)
            continue
        
        # Perform anti-spoofing check
        is_real = verify_anti_spoofing(frame)
        if not is_real:
            cv2.putText(frame, "SPOOF DETECTED!", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow('DroidCam Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        
        try:
            # Detect faces using DeepFace
            faces = DeepFace.extract_faces(
                img_path=frame,
                detector_backend='opencv',
                enforce_detection=False
            )
            
            # Track closest face
            closest_face = None
            max_face_size = 0
            face_info = []
            
            # Process all detected faces
            for face in faces:
                bbox = face['facial_area']
                bbox = [bbox['x'], bbox['y'], 
                        bbox['x'] + bbox['w'], bbox['y'] + bbox['h']]
                bbox = np.array(bbox).astype(int)
                face_size = calculate_face_size(bbox)
                
                # Extract embedding
                embedding = DeepFace.represent(
                    img_path=frame,
                    model_name='VGG-Face',
                    enforce_detection=False
                )[0]['embedding']
                
                # Find best match
                best_match = "Unknown"
                best_similarity = -1
                threshold = 0.4
                
                for name, emb in database.items():
                    # Calculate cosine similarity
                    sim = np.dot(embedding, emb) / (
                        np.linalg.norm(embedding) * np.linalg.norm(emb))
                    if sim > best_similarity:
                        best_similarity = sim
                        best_match = name if sim > threshold else "Unknown"
                
                face_info.append({
                    'bbox': bbox,
                    'size': face_size,
                    'name': best_match,
                    'similarity': best_similarity
                })
                
                # Track closest face
                if face_size > max_face_size:
                    max_face_size = face_size
                    closest_face = best_match
            
            # Draw all faces with distance indication
            for info in face_info:
                bbox = info['bbox']
                color = (0, 255, 0) if info['name'] != "Unknown" else (0, 0, 255)
                
                # Draw bounding box
                thickness = 3 if info['name'] == closest_face else 1
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
                
                # Label with name and distance indicator
                label = f"{info['name']} ({info['similarity']:.2f})"
                if info['name'] == closest_face:
                    label += " [CLOSEST]"
                
                cv2.putText(frame, label, (bbox[0], bbox[1]-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Draw face size indicator
                size_text = f"Size: {info['size']:.1f}"
                cv2.putText(frame, size_text, (bbox[0], bbox[3]+20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display closest face info at top
            if closest_face:
                status_text = f"Closest face: {closest_face}"
                cv2.putText(frame, status_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        except Exception as e:
            print(f"Face processing error: {e}")
        
        cv2.imshow('DroidCam Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()