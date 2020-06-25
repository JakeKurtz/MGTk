import math
import random
import numpy as np

def PoissonDiskSampling(radius, sampleRegionSize, numSamplesBeforeRejection = 30):
	cellSize = radius / math.sqrt(2)

	gridWidth = int(math.ceil(sampleRegionSize[0] / cellSize))
	gridHeight = int(math.ceil(sampleRegionSize[1] / cellSize))

	grid = [[0 for x in range(gridWidth)] for y in range(gridHeight)] 
	points = []
	spawnPoints = []

	spawnPoints.append(sampleRegionSize / 2)

	while (len(spawnPoints) > 0):
		spawnIndex = random.randrange(0.0, len(spawnPoints))
		spawnCenter = spawnPoints[spawnIndex]

		candidateAccepted = False

		for i in range(numSamplesBeforeRejection):
			angle = random.random() * math.pi * 2
			dir = np.array([math.sin(angle), math.cos(angle)])
			candidate = spawnCenter + dir * random.randrange(radius, 2 * radius)

			if (isValid(candidate, sampleRegionSize, cellSize, points, radius, grid)):
				points.append(candidate)
				spawnPoints.append(candidate)
				grid[int(candidate[0] / cellSize)][int(candidate[1] / cellSize)] = len(points)
				candidateAccepted = True
				break

		if (not candidateAccepted):
			del spawnPoints[spawnIndex]

	return points

def isValid(candidate, sampleRegionSize, cellSize, points, radius, grid):
	if (candidate[0] >= 0 and candidate[0] < sampleRegionSize[0] and candidate[1] >= 0 and candidate[1] < sampleRegionSize[1]):
		cell_x = int(candidate[0] / cellSize)
		cell_y = int(candidate[1] / cellSize)

		searchStart_x = max(0, cell_x - 2)
		searchEnd_x = min(cell_x + 2, len(grid[0])-1)		
		
		searchStart_y = max(0, cell_y - 2)
		searchEnd_y = min(cell_y + 2, len(grid[1]) - 1)

		for x in range(searchStart_x, searchEnd_x, 1):
			for y in range(searchStart_y, searchEnd_y, 1):
				pointIndex = grid[x][y] - 1
				if (pointIndex != -1):
					distance = np.linalg.norm(candidate - points[pointIndex])
					if (distance < radius):
						return False
		return True
	return False
