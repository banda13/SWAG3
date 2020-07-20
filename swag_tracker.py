import time
import numpy as np
from scipy.spatial import distance as dist, distance
from collections import OrderedDict
from swag_model import SwagModel
from swag_utils import calculate_centroids


class SwagTracker:

    def __init__(self, logger):
        self.next_object_ID = 0
        self.next_appear_ID = 0
        self.logger = logger
        self.avg_execution_sec = 0

        # TODO customize these params based on the current clip
        self.min_visibility = 10 # this depend on the fps
        self.max_disappeared = 10 # this have to depend on the place
        self.min_registration_distance = 100 # TODO optimize, 100 it to much I think

        self.all_tracked_objects = []
        self.current_objects = OrderedDict()
        self.disappeared_objects = OrderedDict()

        self.counter = 0
        self.current_objects_counter = 0

    def register(self, centroid, box, time_data):
        for (_, obj) in self.current_objects.items():
            d = distance.euclidean(centroid, obj.centroids)
            if d < self.min_registration_distance:
                # print("Avoiding double registration with distance: {}".format(d))
                return
        self.current_objects[self.next_object_ID] = SwagModel(self.next_object_ID, centroid, box, time_data)
        self.disappeared_objects[self.next_object_ID] = 0
        self.next_object_ID += 1

    def deregister(self, objectID, time_data):
        self.current_objects[objectID].last_appear = time_data
        if self.current_objects[objectID].appearance_counter > 3:
            self.current_objects[objectID].count_me = True
        self.all_tracked_objects.append(self.current_objects[objectID])

        del self.current_objects[objectID]
        del self.disappeared_objects[objectID]
        self.current_objects_counter -= 1

    def update(self, yolo_datas, time_data, frame_id):
        start_t = time.time()
        if len(yolo_datas) == 0:
            for objectID in list(self.disappeared_objects.keys()):
                self.disappeared_objects[objectID] += 1
                self.current_objects[objectID].predict_new_centroid(frame_id)

                if self.disappeared_objects[objectID] > self.max_disappeared:
                    self.deregister(objectID, time_data)

            self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2
            return self.current_objects

        input_centroids = np.zeros((len(yolo_datas), 2), dtype="int")
        input_labels = []
        input_confidences = []
        input_boxes = []

        for (i, d) in enumerate(yolo_datas):
            (startX, startY, endX, endY) = d[0]
            input_centroids[i] = calculate_centroids(startX, endX, startY, endY)
            input_labels.append(d[1])
            input_confidences.append(d[2])
            input_boxes.append(d[0])

        if len(self.current_objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i], input_boxes[i], time_data)
        else:
            object_ids = list(self.current_objects.keys())
            object_centroids = [i.centroids for i in self.current_objects.values()]

            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            used_rows = set()
            used_cols = set()
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                objectID = object_ids[row]
                appearance_counter = self.current_objects[objectID].appearance_counter + 1

                self.current_objects[objectID].set_new_centroid(input_centroids[col], input_boxes[col], frame_id)
                self.current_objects[objectID].appearance_counter = appearance_counter
                self.disappeared_objects[objectID] = 0

                if appearance_counter == self.min_visibility:
                    self.current_objects_counter += 1
                    self.counter += 1
                elif appearance_counter > self.min_visibility:
                    self.current_objects[objectID].add_label(input_labels[col], input_confidences[col])

                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    objectID = object_ids[row]
                    self.disappeared_objects[objectID] += 1
                    self.current_objects[objectID].track_lost = True
                    # in this case maybe we can give some estimation
                    # self.current_objects[objectID].predict_new_centroid(frame_id)

                    if self.disappeared_objects[objectID] > self.max_disappeared:
                        self.deregister(objectID, time_data)

            else:
                for col in unused_cols:
                    self.register(input_centroids[col], input_boxes[col], time_data)
        self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2
        return list(self.current_objects.values())