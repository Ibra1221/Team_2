import cv2
import face_recognition
import numpy as np
import base64
from io import BytesIO
from flask import Flask, request, jsonify,render_template
from PIL import Image
import os
import glob

class facerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resize = 0.25

    def encodings_imgs(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        for path in images_path:
            img = cv2.imread(path)
            rgb_path = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            basename = os.path.basename(path)
            (filename, ext) = os.path.splitext(basename)
            encodingss = face_recognition.face_encodings(rgb_path)
            if encodingss:  # Ensure there is at least one face encoding
                self.known_face_encodings.append(encodingss[0])
                self.known_face_names.append(filename)

    def detect(self, frame):
        sm_frame = cv2.resize(frame, (0, 0), fx=self.frame_resize, fy=self.frame_resize)
        rgb_frame = cv2.cvtColor(sm_frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, locations)
        face_names = []
        for f_e in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, f_e)
            if True in matches:
                match_in = matches.index(True)
                name = self.known_face_names[match_in]
            else:
                name = "Unknown"
            face_names.append(name)
        face_locations = np.array(locations)
        face_locations = face_locations / self.frame_resize
        return face_locations.astype(int), face_names

    def detect_face(self, image):
        rgb_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        return len(face_locations) > 0

face_recognition_service = facerec()
face_recognition_service.encodings_imgs('images')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('faceRec.html')
@app.route('/detect_face', methods=['POST'])
def detect_face():
    if request.method == 'POST':
        data = request.get_json()
        img_data = data['image']
        img_data = img_data.replace('data:image/png;base64,', '')
        img_bytes = base64.b64decode(img_data)
        image = Image.open(BytesIO(img_bytes))
        face_detected = face_recognition_service.detect_face(image)
        return jsonify({'face_detected': face_detected})

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    if request.method == 'POST':
        data = request.get_json()
        img_data = data['image']
        img_data = img_data.replace('data:image/png;base64,', '')
        img_bytes = base64.b64decode(img_data)
        image = Image.open(BytesIO(img_bytes))
        _, face_names = face_recognition_service.detect(np.array(image))
        name = face_names[0] if face_names else 'Unknown'
        return jsonify({'name': name})
    elif request.method == 'GET':
        return jsonify({'message': 'Please send a POST request with a base64-encoded image to recognize faces.'})

if __name__ == "__main__":
    app.run(debug=True)
