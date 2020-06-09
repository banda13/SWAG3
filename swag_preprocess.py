import cv2
import random
import numpy as np
from tqdm import tqdm

from swag_model import SwagModel
from swag_speed_detector import SpeedCalculator
from swag_tracker import SwagTracker
from swag_utils import calculate_centroids
from swag_visualizer import SwagVisualizer
from swag_yolo import YOLO
from sklearn.cluster import DBSCAN


class SWAGPreprocessor:

    def __init__(self, input_path, configPath, weightPath, metaPath):
        # initializing video
        self.cap = cv2.VideoCapture(input_path)
        self.totalFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_sec = self.totalFrames * self.fps
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))

        # initializing yolo
        self.yolo = YOLO(configPath, weightPath, metaPath, self.width, self.height)

        # initializing tracker
        self.tracker = SwagTracker()
        self.tracker.min_visibility = 1
        self.tracker.max_disappeared = 1

        # initializing visualizer
        self.visualizer = SwagVisualizer()

        # initialize model
        SwagModel.centroid_history = 99999 # just carefull, but need to remember to occurence place

        # preprocessor config
        self.prep_length_in_sec = min(30, self.total_sec) # TODO set min up to 30 for long videos -> more accurate prep
        self.prep_speed_factor = 2 #  dont!
        self.prep_scene_count = 3  # check 3 random scenario
        self.prep_scene_lenght = self.prep_length_in_sec / self.prep_scene_count

        self.objects = [[] for i in range(self.prep_scene_count)]
        self.start_frames = [i * int(self.totalFrames / self.prep_scene_count) for i in range(self.prep_scene_count)]
        self.frame_per_scene = int(self.fps / self.prep_speed_factor) * self.prep_length_in_sec

        _, self.test_img = self.cap.read()
        self.selected_cars = {}

    def select_car_callback(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.waitKey(0)
            for o in list(self.tracker.current_objects.values()):
                if o.box[0] < x < o.box[2] and o.box[1] < y < o.box[3]:
                    selected_car = o
                    print("Type the real word distances for the selected car and press enter to continue")
                    width = input("Width:")
                    height = input("Height:")
                    if selected_car not in self.selected_cars.keys():
                        self.selected_cars[selected_car] = []

                    self.selected_cars[selected_car].append({
                        "frame": 0,
                        "centroid": selected_car.centroids,
                        "box": selected_car.box,
                        "width": width,
                        "height": height
                    })
                    print("Car selected: {}".format(o.objectId))
                    return selected_car

    def bounding_box(self, points):
        x_coordinates, y_coordinates = zip(*points)
        return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]

    def process(self):
        # crate a pixel-meter scale map


        disappear_centers = []
        appear_centers = []
        move_vectors = []
        for scene in self.objects:
            prev_objects = []
            for frame in scene:
                [move_vectors.append((0, 0) if x.move_vector[0]+x.move_vector[1] < 2 else (np.sign(x.move_vector[0]),np.sign(x.move_vector[1]))) for x in list(set(frame).intersection(prev_objects)) if x.move_vector is not None]
                [appear_centers.append(x.centroid_history[-1] if len(x.centroid_history) > 1 else x.centroids) for x in np.setdiff1d(frame,prev_objects)]
                [disappear_centers.append(x.centroids) for x in np.setdiff1d(prev_objects,frame)]
                prev_objects = frame
        disappear_clusters = DBSCAN(eps=min(self.width, self.height)*0.1, min_samples=int(len(disappear_centers) / 9)+1).fit_predict(np.array(disappear_centers))
        appear_clusters = DBSCAN(eps=min(self.width, self.height) * 0.1,
                                    min_samples=int(len(appear_centers) / 9)+1).fit_predict(np.array(appear_centers))
        vector_clusters = DBSCAN(eps=0.01,min_samples=int(len(move_vectors) / 9)+1).fit_predict(np.array(disappear_centers))
        orginized_vectors = [[] for i in range(len(np.unique(vector_clusters)))]
        for vec, clust in zip(move_vectors, vector_clusters):
            orginized_vectors[clust] = vec

        # visualize
        disappear_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(len(np.unique(disappear_clusters)))]
        appear_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for x in range(len(np.unique(appear_clusters)))]
        disappear_boxes = [(self.bounding_box([x for x, c in zip(disappear_centers, disappear_clusters) if c == i]), i) for i in np.unique(disappear_clusters)]

        for (d, c) in zip(disappear_centers, disappear_clusters):
            self.test_img = cv2.circle(self.test_img, (d[0], d[1]), 4, disappear_colors[c], -1)
        for b in disappear_boxes:
            b = b[0]
            self.test_img = cv2.rectangle(self.test_img, (b[0][0], b[0][1]), (b[1][0], b[1][1]), (255, 0, 0), 7)
            cv2.imshow("disappear", self.test_img)
            cv2.waitKey(0)

        for (d, c) in zip(appear_centers, appear_clusters):
            self.test_img = cv2.circle(self.test_img, (d[0], d[1]), 4, appear_colors[c], -1)
        cv2.imshow("appear", self.test_img)
        cv2.waitKey(0)

    def run(self):
        for k in self.start_frames:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, k)
            for i in tqdm(range(k, k+self.frame_per_scene)):
                ret, frame = self.cap.read()

                if i % self.prep_speed_factor != 0:
                    continue
                curr_time = i / self.fps

                result = self.yolo.detect(frame)
                objects = self.tracker.update(result,curr_time, i)
                self.objects[self.start_frames.index(k)].append(list(objects.values()))
                normal_objects = [o for o in list(objects.values()) if o not in self.selected_cars]
                selected_objects = [o for o in list(objects.values()) if o in self.selected_cars]

                frame = self.visualizer.draw_swag_objects(normal_objects, frame, self.tracker.counter, self.tracker.current_objects_counter)
                for o in selected_objects:
                    frame = self.visualizer.draw_swag_object(o, frame, default_color=(0, 255, 255))
                cv2.imshow("Frame", frame)
                cv2.setMouseCallback('Frame', self.select_car_callback, i + k)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    input_path = "test_data/Road traffic video for object recognition.mp4"
    configPath = "cfg/yolov4.cfg"
    weightPath = "bin/yolov4.weights"
    metaPath = "data/coco.data"
    output = "result3.avi"
    swag = SWAGPreprocessor(input_path, configPath, weightPath, metaPath)
    swag.run()
    swag.process()