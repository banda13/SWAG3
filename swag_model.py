import json
import numpy as np
import operator
from scipy.spatial import distance

swag_directions = {
    (0, 0): 'Not moving',
    (1, 0): 'Right',
    (0, 1): 'Down',
    (1, 1): 'Down Right',
    (-1, 0): 'Left',
    (0, -1): 'Up',
    (-1, -1): 'Up Left',
    (-1, 1): 'Down Left',
    (1, -1): 'Up Right'
}


class SwagModel:
    history_limit = 30

    def __init__(self, objectID, centroids, box, first_appear):
        self.objectId = objectID
        self.centroids = centroids.tolist()
        self.move_vector = None
        self.move_direction = {}
        self.box = box.tolist() # xmin, ymin, xmax, ymax
        self.appearance_counter = 0

        self.centroid_history = [] # need to handle this with a limit
        self.labels = {}
        self.biggest_box = None

        self.first_appear = first_appear # time in sec
        self.last_appear = None
        self.last_update_frame_id = 0
        self.track_lost = False

        self.avg_speed = 0.0
        self.max_speed = 0.0

        self.color = None
        self.make = None
        self.number_plate = None
        self.count_me = False

    def set_new_centroid(self, centroids, box, frame_id):
        self.move_vector = self.set_movement_vector()
        self.set_movement_direction()
        self.centroids = centroids.tolist()
        self.centroid_history.insert(0, self.centroids)
        if len(self.centroid_history) > self.history_limit:
            del self.centroid_history[-1]
        self.box = box.tolist()
        self.last_update_frame_id = frame_id
        self.track_lost = False

    def predict_new_centroid(self, frame_id):
        if self.move_vector is None:
            return
        diff = frame_id - self.last_update_frame_id
        scaled_move_vec = diff * self.move_vector
        prev_centroid = self.centroids

        self.centroids = [self.centroids[0] + scaled_move_vec[0], self.centroids[1] + scaled_move_vec[1]]
        self.box = [int(self.box[0] + scaled_move_vec[0]),
                    int(self.box[1] + scaled_move_vec[1]),
                    int(self.box[2] + scaled_move_vec[0]),
                    int(self.box[3] + scaled_move_vec[1])]

        self.centroid_history.insert(0, prev_centroid)
        if len(self.centroid_history) > self.history_limit:
            del self.centroid_history[-1]
        self.last_update_frame_id = frame_id

    def set_movement_vector(self):
        if len(self.centroid_history) < 3:
            return None
        v0 = (self.centroid_history[0][0] - self.centroid_history[1][0],
              self.centroid_history[0][1] - self.centroid_history[1][1])
        v1 = (self.centroid_history[1][0] - self.centroid_history[2][0],
              self.centroid_history[1][1] - self.centroid_history[2][1])
        v_delta = ((v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2)
        for i in range(len(self.centroid_history)+2, len(self.centroid_history)-1):
            v2 = (self.centroid_history[i][0] - self.centroid_history[i+1][0],
                  self.centroid_history[i][1] - self.centroid_history[i+1][1])
            v_delta = ((v_delta[0] + v2[0]) / 2, (v_delta[1] + v2[1]) / 2)
        return v_delta

    def set_movement_direction(self):
        if self.move_vector is not None:
            l = abs(self.move_vector[0] + self.move_vector[1])
            l = l if l != 0 else 1 # hm not good this static 1
            d = swag_directions[(int(np.sign(self.move_vector[0])),int(np.sign(self.move_vector[1])))]
            if d in self.move_direction.keys():
                self.move_direction[d] += l
            else:
                self.move_direction[d] = l

    def get_movement_direction(self):
        if len(self.move_direction) == 0:
            return "Unknown"
        return max(self.move_direction.items(), key=operator.itemgetter(1))[0]

    def add_label(self, label, confidence):
        if label not in self.labels:
            self.labels[label] = confidence
        else:
            self.labels[label] = (self.labels[label] + confidence) / 2

    def get_label(self):
        if len(self.labels) == 0:
            return "Unknown"
        return max(self.labels.items(), key=operator.itemgetter(1))[0]

    def get_label_confidence(self):
        if len(self.labels) == 0:
            return 0.0
        return max(self.labels.items(), key=operator.itemgetter(1))[1]

    def __lt__(self, other):
        return self.objectId < other.objectId

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    def from_json(self, json_str):
        self.__dict__ = json.loads(json_str)

    def update_from_json(self, json_str):
        self.__dict__.update(json.loads(json_str))

    def dump_to_file(self, file):
        with open(file, 'w') as outfile:
            json.dump(self.__dict__, outfile, indent=4)
