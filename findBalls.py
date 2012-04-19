import ImageFile, Image, ImageDraw
from ballsIdentify import is_table, is_hole, col_diff, change_color_three_balls, TABLE_LEFT, TABLE_RIGHT, TABLE_TOP, TABLE_BOTTOM
from sys import argv, maxint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TOLERANCE = 60

BALLS_COLOR = [0] * 10
BALLS_COLOR[0] = (245, 244, 231)
BALLS_COLOR[1] = (248, 192, 0) #(200, 168, 56)
BALLS_COLOR[2] = (67, 84, 152)
BALLS_COLOR[3] = (0, 255, 255)
BALLS_COLOR[4] = (105, 54, 107)
BALLS_COLOR[5] = (207, 95, 28)
BALLS_COLOR[6] = (28, 83, 25)
BALLS_COLOR[7] = (206, 54, 206)
BALLS_COLOR[8] = (0, 255, 0)
BALLS_COLOR[9] = (197, 154, 9) #(201, 172, 68)

def addColor(c1, c2):
	return c1[0]+c2[0], c1[1]+c2[1], c1[2]+c2[2]

def getAverageSquare(image, center=(8,8)):
	"""
	Return the average color of a square of size 17x17
	Return (maxint, maxint, maxint) if un-appropriate color found
	"""
	total = (0,0,0)
	x,y = center
	count = 0
	tablePixelCount = 0
	for r in range(x-8, x+9):
		for c in range(y-8, y+9):
			if ((r-x)**2+(c-y)**2 <= 8**2): # if the pixel is in circle
				curColor = image.getpixel((r,c))
#			       print curColor, col_diff(curColor, WHITE), col_diff(curColor, BLACK)
				if (is_table(curColor)):
					tablePixelCount += 1
					if (tablePixelCount > 10): # if too much of the pixels are table then it's not a ball
						return (maxint, maxint, maxint)
				if (same(curColor, WHITE, 50) or same(curColor, BLACK, 20)): # exclude the label on each ball
					continue
				total = addColor(total, curColor)
				count += 1
	if (count < 20):
		return (maxint, maxint, maxint)
	avgColor = (total[0]/count, total[1]/count, total[2]/count)
	return avgColor

def same(color1, color2, tolerance=50):
	"""Are the two near the same?"""
	return col_diff(color1, color2) < tolerance

def notInFoundBalls(point, foundPositions):
	x,y = point
	for a,b in foundPositions:
		rSquared = (x-a)**2 + (y-b)**2
		if rSquared <= 8**2:
			return False
	return True

def whichBall(color):
	minIndex = None
	minSoFar = maxint
	for i in range(10):
		diff = col_diff(color, BALLS_COLOR[i])
		if diff < minSoFar:
			minSoFar = diff
			minIndex = i
	if minSoFar > 30:
		pass
		#print "Warning: > 30, might not be right!", minSoFar
	return minIndex

def getBallPositions(image):
	
	import time
	width, height = image.size
	change_color_three_balls(image, 0, image.size[0]-1, 0, image.size[1]-1)
	founds = {}
	foundPositions = []
	step = 5
	start_time = time.time()
	timedOut = False
	
	# find the white ball!
	foundWhiteBall = False
	for y in range(TABLE_TOP-5, TABLE_BOTTOM+5, 1):
		if foundWhiteBall:
			break
		for x in range(TABLE_LEFT-5, TABLE_RIGHT+5, 1):
			point = (x, y)
			color = image.getpixel(point)
			if same(BALLS_COLOR[0], color, 40):
				is_center_point = True
				for x1 in range(x - 5, x + 5):
					if not same(BALLS_COLOR[0], image.getpixel((x1, y)), 80):
						is_center_point = False
				for y1 in range(y - 5, y + 5):
					if not same(BALLS_COLOR[0], image.getpixel((x, y1)), 80):
						is_center_point = False
				if is_center_point:
					foundPositions.append([0, point])
					foundWhiteBall = True
					print 'ball', 0, 'is centered at', point
					break

	for y in range(TABLE_TOP, TABLE_BOTTOM, step):
		if timedOut:
			break
		for x in range(TABLE_LEFT, TABLE_RIGHT, step):
			if time.time() - start_time > 4 and len(founds) > 0:
				timedOut = True
				break
				
			color = image.getpixel( (x,y))
			if (is_table(color) or is_hole((x,y))):
				continue
			posInFounds = map(lambda x: x[0], founds.values())
			if not notInFoundBalls((x,y), posInFounds):
				continue

			nearestBallIndex = whichBall(color)
			nearestBallColor = BALLS_COLOR[nearestBallIndex]
			
			if nearestBallIndex == 1:
			    print("Probably ball 1 found!")

			# BALL 0 IS DIFFERENT FROM THE REST!
			if nearestBallIndex == 0:
				continue

			total = [0,0]
			count = 0
			for x1 in range(x-17, x+18):
				for y1 in range(y-17, y+18):
					c1 = image.getpixel((x1,y1))
					if same(nearestBallColor, c1, 30) and not is_table(c1) and not is_hole((x1,y1)):
						total[0] += x1
						total[1] += y1
						count += 1
			if nearestBallIndex == 8 and count < 70:
				continue
			if nearestBallIndex == 7 and count < 70:
				continue
			if count == 0:
				continue
			ballCenter = total[0]/count, total[1]/count
			founds[nearestBallIndex] = (ballCenter, count)

	# add non-white balls to found position
	for index in founds.keys():
		foundPositions.append([index, founds[index][0]])
		print 'ball', index, 'is centered at', founds[index][0]

	return foundPositions

if __name__ == "__main__":
	positions = None

	if (len(argv)==2):
		if (argv[1]=='getcolors'):
#		       This is to find the average values of all balls
			i = 0
			while (i < 10):
				filename = 'Balls/ball' + str(i) + '.png'
				image = Image.open(filename)
				change_color_three_balls(image, 0, image.size[0]-1, 0, image.size[1]-1)
				print 'BALLS_COLOR[' + str(i) + '] =', getAverageSquare(image)
				i += 1
		else:
			image = Image.open('Balls/' + argv[1] + '.png')
#		       w, h = image.size
#		       change_color_three_balls(image, 0, w, 0, h)
			change_color_three_balls(image)
			positions = getBallPositions(image)
	elif (len(argv) == 3):
		filename = argv[2]
		image = Image.open('Balls/' + filename + '.png')
		if (argv[1] == 'filter_table'):
			output = ImageDraw.Draw(image)
			w, h = image.size
			for x in range(0, w):
				for y in range(0, h):
					if is_table(image.getpixel((x,y))):
						output.point((x,y), None)
			image.save('Balls/' + filename + ' filtered.png')
		elif (argv[1] == 'changeColor'):
			w, h = image.size
#		       change_color_three_balls(image, 0, w, 0, h)
			change_color_three_balls(image)
			image.save('Balls/' + filename + ' changed.png')
	else:
		fp = Image.open('Balls/pic1.png')
#	       change_color_three_balls(image)
		positions = getBallPositions(fp)
	print "Done!"

