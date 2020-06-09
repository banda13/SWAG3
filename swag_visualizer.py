import cv2


class SwagVisualizer:

    def __init__(self, logger):
        self.logger = logger

    def draw_swag_object(self, swag, frame, default_color=(0, 255, 0)):
        text = "ID {}".format(swag.objectId)
        cv2.circle(frame, (swag.centroids[0], swag.centroids[1]), 4, default_color, -1)
        cv2.putText(frame, text, (swag.centroids[0] - 10, swag.centroids[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        tl = (swag.box[0], swag.box[1])
        br = (swag.box[2], swag.box[3])
        label = swag.get_label()
        score = swag.get_label_confidence()
        if len(swag.move_direction) > 0:
            # text2 = '{} {:.2f} | {:.2f}km/h'.format(label, score, swag.avg_speed)
            text2 = '{} {:.2f} | {}'.format(label, score, swag.get_movement_direction())
            # text2 = '{} {:.2f}'.format(label, score)
        else:
            text2 = '{} {:.2f}'.format(label, score)
        if swag.track_lost:
            frame = cv2.rectangle(frame, tl, br, (255, 0, 0), 7)
        else:
            frame = cv2.rectangle(frame, tl, br, default_color, 7)
        frame = cv2.putText(frame, text2, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        return frame

    def draw_swag_objects(self, objects, frame, total, current):
        for swag in objects:
            cv2.putText(frame, "All: {}".format(total), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
                        2)
            cv2.putText(frame, "Currect: {}".format(current), (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            frame = self.draw_swag_object(swag, frame)
        return frame