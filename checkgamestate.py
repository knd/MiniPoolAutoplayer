import Image
import ImageDraw

from ballsIdentify import col_diff
IMAGE_TOP = 1
IMAGE_LEFT = 1
IMAGE_DOWN = 415
IMAGE_RIGHT = 695
CUE_COLOR = (232, 226, 195)

#NOTE: FOR THESE METHODS TO WORK, MOUSE HAS TO BE PLACED AT (351, 0)

def is_cue_color(color, tolerance = 100):
    """ Return whether this color is cue's color. """
    return col_diff(color, CUE_COLOR) <= tolerance

def is_cue_line(point1, point2, image):
    """ Return whether the segment connect point1, point2 is a cue line. """
    if point1[0] <= point2[0]:
        pointL, pointR = point1, point2
    else:
        pointL, pointR = point2, point1
    deltaY = pointR[1] - pointL[1]
    deltaX = pointR[0] - pointL[0]
    if deltaX != 0:
        for x in range(pointL[0], pointR[0] + 1):
            dx = x - pointL[0]
            dy = dx * deltaY/deltaX
            y = pointL[1] + dy
            if not is_cue_color(image.getpixel((x,y))):
                return False
    else:
        up = min(point1[1], point2[1])
        down = max(point1[1], point2[1])
        x = point1[0]
        for y in range(up, down + 1):
            if not is_cue_color(image.getpixel((x, y))):
                return False

    return True

def cue_exist(image):
    """ Return whether the cue appears in the image. """
    for x1 in range(IMAGE_LEFT, IMAGE_RIGHT, 2):
        for y1 in range(IMAGE_TOP, IMAGE_DOWN, 25):
            point1 = (x1, y1)
            if is_cue_color(image.getpixel(point1)):

                left2 = max(IMAGE_LEFT, x1 - 70)
                right2 = min(IMAGE_RIGHT, x1 + 70)
                y2 = y1 + 25
                for x2 in range(left2, right2):
                    point2 = (x2, y2)
                    if is_cue_line(point1, point2, image):
                        return True
    return False

def is_game_ready(image):
	import os 
	import time
	time.sleep(0.5)
	os.system("xdotool mousemove 621 674")
	return cue_exist(image)

if __name__ == "__main__":
    image = Image.open("nocue3.png")
    print is_game_ready(image)
