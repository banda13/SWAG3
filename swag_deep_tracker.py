import time
import cv2
from deepsort import nn_matching
from deepsort.detection import Detection
from deepsort.tracker import Tracker
from encoder import create_box_encoder


class SwagDeepTracker:

    def __init__(self, logger):
        metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", 0.3, 100) # cosine
        self.tracker = Tracker(metric)
        self.current_objects = []
        self.all_tracked_objects = []
        self.logger = logger
        self.avg_execution_sec = 0

        # callable
        # needs the BGR image & the bounding boxes in the format: (x, y, w, h)
        self.encoder = create_box_encoder("deepsort/resources/mars-small128.pb")


    def get_features(self, frame, boxes):
        f = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return self.encoder(f, boxes)

    def update(self, yolo_datas, time_data, frame_id, frame):
        start_t = time.time()
        self.tracker.predict()

        detections = []
        features = self.get_features(frame, [i[3] for i in yolo_datas])
        for i in range(len(yolo_datas)):
            yolo_d = yolo_datas[i]
            detections.append(Detection(yolo_d[0], yolo_d[2], features[i]))

        self.tracker.update(detections, time_data)
        self.current_objects = self.tracker.get_tracks_as_swag()
        for o in self.current_objects:
            if o not in self.all_tracked_objects:
                self.all_tracked_objects.append(o)
        self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2
        return self.current_objects
