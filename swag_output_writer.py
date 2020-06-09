import os
import cv2
import json
import time

from swag_utils import calculate_box_size_for_swag, calculate_box_size


class OutputWriter:

    def __init__(self, logger,  name, write_output, output_params):
        self.name = name
        self.logger = logger
        self.avg_execution_sec = 0

        self.write_output = write_output
        if self.write_output:
            self.output_path = "results/" + self.name + "/output.mp4"
            self.out_file = cv2.VideoWriter(self.output_path, 0x00000021, output_params["fps"],
                                            (output_params["width"], output_params["height"]))

        self.im_directory = "results/" + self.name + "/images/"
        self.obj_directory = "results/" + self.name + "/objects/"
        self.objects_txt = "results/" + self.name + "/objects.txt"

        self.preview_img = None

        self.w = 224
        self.h = 224

        os.mkdir(self.im_directory)
        os.mkdir(self.obj_directory)
        with open(self.objects_txt, "w") as f:
            pass

    def check_and_write(self, current_objects, final_objects, frame, frame_with_draw):
        start_t = time.time()
        for o in current_objects:
            if not o.track_lost:
                current_box_size = calculate_box_size_for_swag(o)
                max_box_size = calculate_box_size(o.biggest_box[0], o.biggest_box[2], o.biggest_box[1], o.biggest_box[3]) if o.biggest_box is not None else 0
                if current_box_size > max_box_size:
                    try:
                        o.biggest_box = o.box
                        img = frame[o.box[1]:o.box[3], o.box[0]:o.box[2]]
                        img = cv2.resize(img, (self.w, self.h))
                        cv2.imwrite(self.im_directory + "{}.png".format(o.objectId), img)
                    except Exception as e:
                        self.logger.error("Failed to save image: {}".format(self.im_directory + "{}.png".format(o.objectId)))

        for o in final_objects:
            if o.count_me:
                self.logger.info("Object counted: {}".format(o.objectId))
                o.dump_to_file(self.obj_directory + str(o.objectId) + ".json")
                with open(self.objects_txt, "a") as f:
                    f.write(str(o.objectId) + "\n")
                o.count_me = False

        if self.write_output:
            self.out_file.write(frame_with_draw)
        if self.preview_img is None:
            self.preview_img = True
            cv2.imwrite("results/" + self.name + "/preview.png", frame)
        self.avg_execution_sec = (self.avg_execution_sec + (time.time() - start_t)) / 2

    def finalize(self):
        if self.write_output:
            self.out_file.release()