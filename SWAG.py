import os
import cv2
import time
import shutil

from swag_deep_tracker import SwagDeepTracker
from swag_logger import Logger
from swag_output_writer import OutputWriter
from swag_speed_detector import SpeedCalculator
from swag_tracker import SwagTracker
from swag_visualizer import SwagVisualizer
from swag_yolo import YOLO


class SWAG:

    def __init__(self, input_path, config_path, weight_path, meta_path, output=True):
        self.skip_ratio = 1
        self.show = True
        self.make_logs = True
        self.name = os.path.splitext(input_path.split("/")[-1])[0]
        self.base_dir = 'results/' + self.name
        if os.path.exists(self.base_dir) and os.path.isdir(self.base_dir):
            shutil.rmtree(self.base_dir)
        os.mkdir(self.base_dir)

        # initialize logger
        self.logger = Logger(self.name, self.make_logs)

        self.logger.info("Initializing cv2 video input: {}".format(input_path))
        self.cap = cv2.VideoCapture(input_path)
        self.totalFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))

        # initializing yolo
        self.yolo = YOLO(self.logger, config_path, weight_path, meta_path, self.width, self.height)

        # initializing tracker
        self.tracker = SwagTracker(self.logger)
        self.deep_tracker = SwagDeepTracker(self.logger)

        # initialize speed detector
        self.speed_detector = SpeedCalculator(self.logger, "cfg/pixel_scale_map.txt", measurement_freq=self.fps/2, fps=self.fps)

        # initialize output writer
        self.output_writer = OutputWriter(self.logger, self.name, output, {"width": self.width, "height": self.height, "fps": self.fps})

        # initializing visualizer
        self.visualizer = SwagVisualizer(self.logger)

    def run(self):
        self.logger.info("SWAG loop starting...")
        start_t = time.time()
        for i in range(self.totalFrames):
            try:
                ret, frame = self.cap.read()
                curr_time = i / self.fps

                if i % self.skip_ratio != 0:
                    continue

                result = self.yolo.detect(frame)
                objects = self.tracker.update(result,curr_time, i)
                # objects = self.deep_tracker.update(result, curr_time, i, frame)
                objects = self.speed_detector.calculate_speeds(i, objects)

                draw_frame = frame.copy()
                if self.show:
                    draw_frame = self.visualizer.draw_swag_objects(objects, draw_frame, self.tracker.counter,
                                                              self.tracker.current_objects_counter)
                    cv2.imshow("Frame", draw_frame)

                self.output_writer.check_and_write(objects, self.tracker.all_tracked_objects, frame, draw_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            except Exception as e:
                self.logger.exception("SWAG loop crashed, break it", e)
                break

        self.logger.info("Finalizing SWAG loop")
        self.cap.release()
        self.output_writer.finalize()
        cv2.destroyAllWindows()

        self.logger.info("------ RUN STATISTIC: {} -------".format(self.name))
        self.logger.info("Total run time: {}".format(time.time() - start_t))
        self.logger.info("Detected vehicles: {}".format(self.tracker.counter))
        self.logger.info("Average YOLO execution time: {}".format(self.yolo.avg_execution_sec))
        self.logger.info("Average Tracker execution time: {}".format(self.tracker.avg_execution_sec))
        self.logger.info("Average Speed calculator execution time: {}".format(self.speed_detector.avg_execution_sec))
        self.logger.info("Average Output write execution time: {}".format(self.output_writer.avg_execution_sec))


if __name__ == '__main__':
    input_path = "test_data/test.mp4"
    configPath = "cfg/yolov4.cfg"
    weightPath = "bin/yolov4.weights"
    metaPath = "data/coco.data"
    swag = SWAG(input_path, configPath, weightPath, metaPath)
    swag.run()