import cv2 
import face_recognition 
import os 
import glob
import numpy as np

class facerec:
    def __init__(self):  #function to save the attributes of the face << face encoding and face name 
        self.known_face_encodings = [] # this list to save the faces codes << each face has a code >> 
        self.known_face_names =[] # this list to save the faces names << each face has a name >> 
        self.frame_resize= 0.25
    def encodings_imgs(self, images_path):
        images_path = glob.glob(os.path.join(images_path,"*.*")) #this line extracts all the paths of images in the project's file and save them in this list

        for path in images_path: #loop to read all the images that their path is stored in (images_path)
            img = cv2.imread(path) #reading each image
            rgb_path = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #converting them to rgb to be suitable for the face_recognation library

            basename = os.path.basename(path)  #here we just store in basename the path of the photo << ex : 
            # path = "/path/to/your/image.jpg" .. so basename will equal "image.jpg"
            (filename,ext) = os.path.splitext(basename) #spliting basename to the filename and path << filename = "image" and ext = "jpg"
            encodingss = face_recognition.face_encodings(rgb_path)[0] #each foto contains a face >> heare we are coding the face we have in the foto 
            
            self.known_face_encodings.append(encodingss) #storing faces in database
            self.known_face_names.append(filename) #storing the filenames
    def detect(self,frame):
            sm_frame = cv2.resize(frame,(0,0), fx = self.frame_resize , fy=self.frame_resize) #resizing the frame 
            rgb_frame = cv2.cvtColor(sm_frame,cv2.COLOR_BGR2RGB) 
            locations = face_recognition.face_locations(rgb_frame) #locating the faces 
            face_encodings = face_recognition.face_encodings(rgb_frame,locations) #encoding faces 
            face_names = []
            name = "Unknown"
            for f_e in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings , f_e) #comparing the face in frame with face in data base
                if True in matches: #if matches it will give it the name to be written on it 
                    match_in = matches.index(True)
                    name = self.known_face_names[match_in]
            face_names.append(name)
            face_locations = np.array(locations)
            face_locations = face_locations / self.frame_resize 
            
            return face_locations.astype(int) , face_names


            

