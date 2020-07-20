import cv2
import os
import time
import numpy as np
from darknet.build.darknet.x64 import darknet


class YOLO:

    netMain = None
    metaMain = None
    altNames = None

    def __init__(self, logger, config_path, weight_path, meta_path, origin_w, origin_h):
        self.logger = logger
        self.logger.info("Initializing YOLO:\n config: {}\n weights: {}\n meta: {}".format(config_path, weight_path, meta_path))
        self.avg_execution_sec = 0

        if not os.path.exists(config_path):
            raise ValueError("Invalid config path `" +
                             os.path.abspath(config_path) + "`")
        if not os.path.exists(weight_path):
            raise ValueError("Invalid weight path `" +
                             os.path.abspath(weight_path) + "`")
        if not os.path.exists(meta_path):
            raise ValueError("Invalid data file path `" +
                             os.path.abspath(meta_path) + "`")
        if self.netMain is None:
            self.netMain = darknet.load_net_custom(config_path.encode(
                "ascii"), weight_path.encode("ascii"), 0, 1)  # batch size = 1
        if self.metaMain is None:
            self.metaMain = darknet.load_meta(meta_path.encode("ascii"))
        if self.altNames is None:
            try:
                with open(meta_path) as metaFH:
                    metaContents = metaFH.read()
                    import re
                    match = re.search("names *= *(.*)$", metaContents,
                                      re.IGNORECASE | re.MULTILINE)
                    if match:
                        result = match.group(1)
                    else:
                        result = None
                    try:
                        if os.path.exists(result):
                            with open(result) as namesFH:
                                namesList = namesFH.read().strip().split("\n")
                                self.altNames = [x.strip() for x in namesList]
                    except TypeError:
                        pass
            except Exception:
                pass

        self.darknet_image = darknet.make_image(darknet.network_width(self.netMain),
                                           darknet.network_height(self.netMain), 3)

        self.origin_h = origin_h
        self.origin_w = origin_w
        self.h_compress_ratio = self.origin_w / darknet.network_width(self.netMain)
        self.w_compress_ration = self.origin_h / darknet.network_height(self.netMain)

    def convertBack(self, x, y, w, h):
        xmin = int(((x - (w / 2)) / darknet.network_width(self.netMain)) * self.origin_w)
        xmax = int(((x + (w / 2)) / darknet.network_width(self.netMain)) * self.origin_w)
        ymin = int(((y - (h / 2)) / darknet.network_height(self.netMain)) * self.origin_h)
        ymax = int(((y + (h / 2)) / darknet.network_height(self.netMain)) * self.origin_h)
        return xmin, ymin, xmax, ymax

    def detect(self, image):
        start_t = time.time()
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(self.netMain),
                                    darknet.network_height(self.netMain)),
                                   interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(self.darknet_image, frame_resized.tobytes())
        detections = darknet.detect_image(self.netMain, self.metaMain, self.darknet_image, thresh=0.25)

        final_detection = []
        for detection in detections:
            x, y, w, h = detection[2][0], \
                         detection[2][1], \
                         detection[2][2], \
                         detection[2][3]
            xmin, ymin, xmax, ymax = self.convertBack(float(x), float(y), float(w), float(h))
            label = detection[0].decode()
            if label in ['car', 'truck', 'bicycle', 'bus', 'motorbike']: # temporary while I can buy a new videocard with enough memory to train
                final_detection.append([np.array([xmin, ymin, xmax, ymax]),
                    label,
                    detection[1],
                    detection[2]])
        self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2
        return final_detection