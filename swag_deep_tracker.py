from deepsort import nn_matching
from deepsort.detection import Detection
from deepsort.tracker import Tracker


class SwagDeepTracker:

    def __init__(self):
        metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", 0.3, 100)
        self.tracker = Tracker(metric)


    def update(self, yolo_datas, time_data, frame_id):
        self.tracker.predict()

        detections = []
        for yolo_d in yolo_datas:
            detections.append(Detection(yolo_d[0], yolo_d[2], yolo_d[1]))

        self.tracker.update(detections)
        tracks = self.tracker.tracks
        print(tracks)