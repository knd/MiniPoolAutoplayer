import Image
import ImageDraw

BALLS_COLOR = [(0,0)] * 10
BALLS_COLOR[1] = (224, 174, 0)
BALLS_COLOR[2] = (40, 58, 132)
BALLS_COLOR[3] = (205, 16, 16)
BALLS_COLOR[4] = (93, 15, 102)
BALLS_COLOR[5] = (223, 83, 0)
BALLS_COLOR[6] = (4, 76, 0)
BALLS_COLOR[7] = (94, 12, 0)
BALLS_COLOR[8] = (30, 17, 6)
BALLS_COLOR[9] = (217, 169, 2)

TABLE_COLOR_1 = (131, 39, 37)
TABLE_COLOR_2 = (156, 46, 44)
TABLE_COLOR_3 = (111, 31, 30)
TABLE_COLOR_4 = (92, 26, 26)
TABLE_COLOR_5 = (48, 11, 8)
TABLE_TOP = 60
TABLE_LEFT = 47
TABLE_BOTTOM = 382
TABLE_RIGHT = 652
table_bottom_right = (652, 382)

HOLES = [(0,0)]*8

HOLES[1] = (351, 64)
HOLES[2] = (649, 62)
HOLES[3] = (51, 375)
HOLES[4] = (348, 384)
HOLES[5] = (649, 375)
HOLE_RADIUS = 22


def col_diff(color1, color2):
    """ Return the color difference between two color"""
    return ((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2) ** (0.5)

# Use this
def is_table(color):
    """ Return whether the color is the same as table's color. """
    return col_diff(color, TABLE_COLOR_1) < 25 or col_diff(color, TABLE_COLOR_2) < 25 or col_diff(color, TABLE_COLOR_3) < 25 \
           or col_diff(color, TABLE_COLOR_4) < 25 or col_diff(color, TABLE_COLOR_5) < 25

def distance(point1, point2):
    """ Return the distance between point1 and point2. """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** (0.5)

def is_hole(point):
    """ Return whether point is in the hole. """
    for hole in HOLES:
        if distance(point, hole) < HOLE_RADIUS:
            return True
    return False

def change_color_three_balls(image, table_left = TABLE_LEFT, table_right = TABLE_RIGHT, table_top = TABLE_TOP, table_bottom = TABLE_BOTTOM):
    output_image = ImageDraw.Draw(image)
    tolerance1 = 60
    tolerance2 = 20
    tolerance3 = 20
    new_color_1 = (0,255,255)
    new_color_2 = (206, 54, 206)
    new_color_3 = (0, 255, 0)

    found_ball_3 = False
    found_ball_7 = False
    found_ball_8 = False

    min_change = 30

    for x in range(table_left, table_right + 1, 4):
        for y in range(table_top, table_bottom + 1, 4):
            # probably ball 3 found!
            if not found_ball_3 and  col_diff(image.getpixel((x,y)), BALLS_COLOR[3]) <= tolerance1:
                pixel_changed = 0
                left = max(x - 17, table_left)
                right = min( x + 17, table_right)
                up = max(y - 17, table_top)
                bottom = min(y + 17, table_bottom)
                for a in range(left, right):
                    for b in range (up, bottom):
                        if col_diff(image.getpixel((a,b)), BALLS_COLOR[3]) <= tolerance1:
                           output_image.point((a,b), new_color_1)
                           pixel_changed += 1
                if pixel_changed >= min_change:
                    found_ball_3 = True

            # probably ball 7 found, hardest case
            elif not found_ball_7 and col_diff(image.getpixel((x,y)), BALLS_COLOR[7]) <= tolerance2:
                pixel_changed = 0
                left = max(x - 17, table_left)
                right = min( x + 17, table_right)
                up = max(y - 17, table_top)
                bottom = min(y + 17, table_bottom)
                for a in range(left, right):
                    for b in range (up, bottom):
                        if col_diff(image.getpixel((a,b)), BALLS_COLOR[7]) < 20 or col_diff(image.getpixel((a,b)), (95,12,0)) <= 30:
                            output_image.point((a,b), new_color_2)
                if pixel_changed >= min_change:
                    found_ball_7 = True

            # probably ball 8 found
            elif not found_ball_8 and col_diff(image.getpixel((x,y)), BALLS_COLOR[8]) <= 20 and not is_hole((x,y)):
                pixel_changed = 0
                left = max(x - 17, table_left)
                right = min( x + 17, table_right)
                up = max(y - 17, table_top)
                bottom = min(y + 17, table_bottom)
                for a in range(left, right):
                    for b in range (up, bottom):
                        if col_diff(image.getpixel((a,b)), BALLS_COLOR[8]) <= tolerance3:
                           output_image.point((a,b), new_color_3)
                           pixel_changed += 1
                #if pixel_changed >= min_change:
                #    found_ball_8 = True

            if found_ball_7 and found_ball_3 and found_ball_8:
                return None

def test_fill_balls(image):
    output_image = ImageDraw.Draw(image)
    for x in range(TABLE_LEFT, TABLE_RIGHT + 1):
        for y in range(TABLE_TOP, TABLE_BOTTOM + 1):
            if is_table(image.getpixel((x,y))):
                output_image.point((x,y), None)

if __name__ == "__main__":
    input_files = ("b2.png", "b3.png", "b4.png", "b5.png", "b6.png", "b7.png", "b8.png", "b9.png")
    output_files = ("output2.png", "output3.png", "output4.png", "output5.png", "output6.png", "output7.png", "output8.png", "output9.png")

    for i in range(0,8):
        image = Image.open(input_files[i])
        change_color_three_balls(image)
        test_fill_balls(image)
        image.save(output_files[i])
