import os
import random as rd
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
from pathlib import Path

##create necessary image table
def generateAllTable(sizeW, sizeH, pixelTolerance=1):
	tab = []
	for i in range(-pixelTolerance, pixelTolerance + 1):
		for j in range(-pixelTolerance, pixelTolerance + 1):
			tab.append([sizeW + i, sizeH + j, i, j])
	tablePath = []
	for i in tab:
		filename = "{}x{}.png".format(i[0], i[1])
		tablePath.append([filename, i[2], i[3]])
		if not Path(filename).exists():
			im = Image.new('RGB', (i[0], i[1]), (255,255,255))
			draw = ImageDraw.Draw(im, 'RGB')
			draw.rectangle([(0, 0), (i[0] - 1, i[1] - 1)], outline=(0,0,0))
			im.save("table/" + filename, "PNG")
			print("Image save {}".format(filename))
	return tablePath

##return all table in plan of size
def getAllTable(planPath, sizeTable):
	allTable = []
	tablePath = generateAllTable(sizeTable[0], sizeTable[1], sizeTable[2])
	print(tablePath)

	for i in tablePath:
		newTable = getTable(planPath, i)
		for j in newTable:
			allTable.append(j)
	allTable.sort()
	return allTable

##get all table of type tablePath in plan
def getTable(planPath, tablePath):
	table = []
	img_rgb = cv2.imread(planPath)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread("table/" + tablePath[0], 0)
	w, h = template.shape[::-1]
	
	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= 0.9025)
	print(loc)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		table.append((pt[0] - tablePath[1], pt[1] - tablePath[2]))
	cv2.imwrite('out/res_{}'.format(tablePath[0]), img_rgb)
	table = list(set(table))
	table.sort()
	return table

def doWhatYouHaveToDo(filepath, size):
	res = getAllTable(filepath, size)
	print(res)

	im = Image.open(filepath)
	draw = ImageDraw.Draw(im)
	sSum = 0
	for i in res:
		sSum += 1
		#draw.rectangle([i, (i[0] + size[0], i[1] + size[1])], fill=(127,127,127), outline=(255,0,0))
		draw.text(i, str(sSum), fill=(255,0,0))
	im.save("res.png", "PNG")
	print(sSum)