import cv2
from scipy.spatial import distance

input_video = "test1.mp4"

ref_pt = []
out_file = "{}_pixel_scale_map.txt".format()
def selection(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_pt.append((x, y))

image = cv2.imread("test.png")
cv2.namedWindow("image")
cv2.setMouseCallback("image", selection)

with open(out_file, "w") as out:
    while True:
        cv2.imshow("image", image)

        key = cv2.waitKey(1) & 0xFF

        if len(ref_pt) == 2:
            scale_factor = distance.euclidean(ref_pt[0], ref_pt[1]) / 6
            cv2.line(image, ref_pt[0], ref_pt[1], (0, 255, 0), thickness=2)
            cv2.putText(image, "1m = {} px".format(scale_factor), (ref_pt[0][0] + 10, ref_pt[0][1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print("Your scale factor is: {}".format(scale_factor))
            out.write("{},{},{},{},{}\n".format(ref_pt[0][0], ref_pt[0][1], ref_pt[1][0], ref_pt[1][0],scale_factor))
            ref_pt = []

        elif key == ord("q"):
            break

cv2.destroyAllWindows()