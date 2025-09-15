# import cv2
# import numpy as np
# from insightface.app import FaceAnalysis
# import pickle
# import time

# def initialize_model():
#     try:
#         app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
#         app.prepare(ctx_id=0, det_size=(320, 320))
#         return app
#     except Exception as e:
#         print(f"Model initialization failed: {e}")
#         return None

# def load_face_database(pickle_path):
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
#     model = initialize_model()
#     if model is None:
#         return
    
#     pickle_path = r"D:\Python\Python_practice\face_embeddings.pkl"
#     database = load_face_database(pickle_path)
#     if not database:
#         print("No valid embeddings in database")
#         return
    
#     # Use system camera (default camera, index 0)
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
#     if not cap.isOpened():
#         print("Failed to open system camera")
#         return
    
#     print("Connected to system camera. Press 'q' to quit...")
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame from camera")
#             break
        
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         faces = model.get(frame_rgb)
        
#         # Track closest face
#         closest_face = None
#         max_face_size = 0
#         face_info = []
        
#         # Process all faces first
#         for face in faces:
#             bbox = face.bbox.astype(int)
#             embedding = face.normed_embedding
#             face_size = calculate_face_size(bbox)
            
#             # Find best match
#             best_match = "Unknown"
#             best_similarity = -1
#             threshold = 0.4
            
#             for name, emb in database.items():
#                 sim = np.dot(embedding, emb)
#                 if sim > best_similarity:
#                     best_similarity = sim
#                     best_match = name if sim > threshold else "Unknown"
            
#             face_info.append({
#                 'bbox': bbox,
#                 'size': face_size,
#                 'name': best_match,
#                 'similarity': best_similarity
#             })
            
#             # Track closest face
#             if face_size > max_face_size:
#                 max_face_size = face_size
#                 closest_face = best_match
        
#         # Draw all faces with distance indication
#         for info in face_info:
#             bbox = info['bbox']
#             color = (0, 255, 0) if info['name'] != "Unknown" else (0, 0, 255)
            
#             # Draw bounding box
#             thickness = 3 if info['name'] == closest_face else 1
#             cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
            
#             # Label with name and distance indicator
#             label = f"{info['name']} ({info['similarity']:.2f})"
#             if info['name'] == closest_face:
#                 label += " [CLOSEST]"
            
#             cv2.putText(frame, label, (bbox[0], bbox[1]-10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
#             # Draw face size indicator
#             size_text = f"Size: {info['size']:.1f}"
#             cv2.putText(frame, size_text, (bbox[0], bbox[3]+20),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
#         # Display closest face info at top
#         if closest_face:
#             status_text = f"Closest face: {closest_face}"
#             cv2.putText(frame, status_text, (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
#         cv2.imshow('System Camera Face Recognition', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

#=====================================================================================================


import cv2
import numpy as np
from insightface.app import FaceAnalysis
import pickle
import time
from scipy.spatial import distance

def initialize_model():
    try:
        app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(320, 320))
        return app
    except Exception as e:
        print(f"Model initialization failed: {e}")
        return None

def load_face_database(pickle_path):
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
    return (width + height) / 2

def variance_of_laplacian(image):
    """Compute the Laplacian variance to check image sharpness"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def compute_ear(eye_points):
    """Compute Eye Aspect Ratio (EAR) for blink detection"""
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

def is_real_face(image, face, blink_counter, prev_ear, blink_threshold=0.2, laplacian_threshold=100):
    """Anti-spoofing check combining Laplacian variance and blink detection"""
    # Crop face region for analysis
    bbox = face.bbox.astype(int)
    face_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]

    # Check image sharpness (low variance suggests a photo or screen)
    laplacian_var = variance_of_laplacian(face_img)
    if laplacian_var < laplacian_threshold:
        return False, blink_counter, prev_ear, "Low sharpness (possible photo/screen)"

    # Blink detection using eye landmarks
    landmarks = face.landmark_2d_106
    left_eye = [landmarks[i] for i in [33, 34, 35, 36, 37, 38]]  # Example indices for left eye
    right_eye = [landmarks[i] for i in [87, 88, 89, 90, 91, 92]]  # Example indices for right eye

    if len(left_eye) == 6 and len(right_eye) == 6:
        left_ear = compute_ear(left_eye)
        right_ear = compute_ear(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Detect blink (EAR drops below threshold then rises)
        if prev_ear is not None:
            if ear < blink_threshold and prev_ear >= blink_threshold:
                blink_counter += 1

        prev_ear = ear
    else:
        return False, blink_counter, prev_ear, "Invalid eye landmarks"

    # Require at least one blink for liveness (adjust based on testing)
    if blink_counter < 1:
        return False, blink_counter, prev_ear, "No blink detected"

    return True, blink_counter, prev_ear, "Real face"

def main():
    model = initialize_model()
    if model is None:
        return
    
    pickle_path = r"D:\Python\Python_practice\face_embeddings.pkl"
    database = load_face_database(pickle_path)
    if not database:
        print("No valid embeddings in database")
        return
    
    # Use system camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    if not cap.isOpened():
        print("Failed to open system camera")
        return
    
    print("Connected to system camera. Press 'q' to quit...")
    
    blink_counter = 0
    prev_ear = None
    last_reset_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera")
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = model.get(frame_rgb)
        
        # Reset blink counter every 10 seconds to avoid permanent lockout
        if time.time() - last_reset_time > 10:
            blink_counter = 0
            last_reset_time = time.time()
        
        closest_face = None
        max_face_size = 0
        face_info = []
        
        for face in faces:
            bbox = face.bbox.astype(int)
            embedding = face.normed_embedding
            face_size = calculate_face_size(bbox)
            
            # Anti-spoofing check
            is_real, blink_counter, prev_ear, spoof_status = is_real_face(
                frame, face, blink_counter, prev_ear
            )
            
            # Find best match
            best_match = "Unknown"
            best_similarity = -1
            threshold = 0.4
            
            if is_real:
                for name, emb in database.items():
                    sim = np.dot(embedding, emb)
                    if sim > best_similarity:
                        best_similarity = sim
                        best_match = name if sim > threshold else "Unknown"
            else:
                best_match = f"Spoof ({spoof_status})"
                best_similarity = 0.0
            
            face_info.append({
                'bbox': bbox,
                'size': face_size,
                'name': best_match,
                'similarity': best_similarity
            })
            
            if face_size > max_face_size and is_real:
                max_face_size = face_size
                closest_face = best_match
        
        for info in face_info:
            bbox = info['bbox']
            color = (0, 255, 0) if info['name'] != "Unknown" and not info['name'].startswith("Spoof") else (0, 0, 255)
            
            thickness = 3 if info['name'] == closest_face else 1
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
            
            label = f"{info['name']} ({info['similarity']:.2f})"
            if info['name'] == closest_face:
                label += " [CLOSEST]"
            
            cv2.putText(frame, label, (bbox[0], bbox[1]-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            size_text = f"Size: {info['size']:.1f}"
            cv2.putText(frame, size_text, (bbox[0], bbox[3]+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if closest_face:
            status_text = f"Closest face: {closest_face}"
            cv2.putText(frame, status_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Display blink counter
        blink_text = f"Blinks: {blink_counter}"
        cv2.putText(frame, blink_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        cv2.imshow('System Camera Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()