import time
from scipy.spatial import distance


class SpeedCalculator:

    def __init__(self, logger, config_file, measurement_freq, fps):
        self.pixel_scale_map = {}
        self.logger = logger
        self.avg_execution_sec = 0
        with open(config_file, 'r') as f:
            line = f.readline()
            while line:
                x0, y0, x1, y1, scale = [float(x) for x in line.split(",")]
                self.pixel_scale_map[self.midpoint((x0, y0), (x1, y1))] = scale
                line = f.readline()
        self.measurement_freq = measurement_freq
        self.fps = fps

    def midpoint(self, pt_a, pt_b):
        return (pt_a[0] + pt_b[0]) * 0.5, (pt_a[1] + pt_b[1]) * 0.5

    def lookup_for_scale_map(self, pos0, pos1):
        mid = self.midpoint(pos0, pos1)
        closest_dist, closest_scale = 999999, None
        for pos, scale in self.pixel_scale_map.items():
            d = distance.euclidean(pos, mid)
            if d < closest_dist:
                closest_dist = d
                closest_scale = scale
        return closest_scale

    def predict_speed(self, swag_obj):
        if len(swag_obj.centroid_history) < 10:
            return

        p0 = swag_obj.centroid_history[0]
        p1 = swag_obj.centroid_history[-1]
        scale = self.lookup_for_scale_map(p0, p1)
        s = distance.euclidean(p0, p1) / scale
        t = (self.fps / self.measurement_freq)
        v = (s / t) * 3.6
        swag_obj.avg_speed = (swag_obj.avg_speed + v) / 2
        swag_obj.max_speed = (v if v > swag_obj.max_speed else swag_obj.max_speed)
        return swag_obj.avg_speed

    def calculate_speeds(self, frame_id, objects):
        start_t = time.time()
        if frame_id % self.measurement_freq == 0:
            for (objectID, swag) in objects.items():
                self.predict_speed(swag)
        self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2
        return objects
