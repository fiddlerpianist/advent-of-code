def move(direction, coord, path):
    x = coord['x']
    y = coord['y']
    # remove any \n if it exists
    dir = direction.rstrip()
    amt = int(dir[1:len(dir)])

    if dir.startswith("R"):
        for i in range(x+1, x+amt+1):
            path.append((i,y))
        coord['x'] += amt
    elif dir.startswith("L"):
        for i in range(x-1, x-amt-1, -1):
            path.append((i,y))
        coord['x'] -= amt
    elif dir.startswith("U"):
        for i in range(y+1, y+amt+1):
            path.append((x,i))
        coord['y'] += amt
    elif dir.startswith("D"):
        for i in range(y-1, y-amt-1, -1):
            path.append((x,i))
        coord['y'] -= amt
    else:
        # Fortunately we don't have any of these
        print ("Error! Wasn't expecting that!")    
    return path

def findDistancesToCommonPoints(path, intersections):
    positions = {}
    previousCoord = (0,0)
    cumulativeDistance = 0
    for i in range(0, len(path)):
        cumulativeDistance += calculateDistance(previousCoord, path[i])
        if path[i] in intersections and path[i] not in positions:
            positions[path[i]] = cumulativeDistance
        # make the current coord the previous one for the next iteration
        previousCoord = path[i]
    return positions

def calculateDistance(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

# Initialize: open file, put both wire directions into lists
with open('day03.txt') as f:
    wireOneDirections = f.readline().split(",")
    wireTwoDirections = f.readline().split(",")

# Setup: get the paths that the wires take, put the coordinate points into a trackable list
wireCoord = { 'x': 0, 'y': 0}
firstpath = []
for i in range(0, len(wireOneDirections)):
    move(wireOneDirections[i], wireCoord, firstpath)

wireCoord = { 'x': 0, 'y': 0}
secondpath = []
for i in range(0, len(wireTwoDirections)):
    move(wireTwoDirections[i], wireCoord, secondpath)

# Part One: find the intersection point closest to the central port (which is at (0, 0))
intersections = set(firstpath).intersection(set(secondpath))
# (Initialize with large number...one that will be larger than any of the numbers we might encounter)
least = 1000000
for tup in intersections:
    sum = abs(tup[0]) + abs(tup[1])
    if sum < least:
        least = sum

print ("Part One: %i" % least)

# Part Two: find the fewest combined steps the wires must take to reach an intersection
distancesOne = findDistancesToCommonPoints(firstpath, intersections)
distancesTwo = findDistancesToCommonPoints(secondpath, intersections)
combinedDistances = []
for key in distancesOne:
    combinedDistances.append(distancesOne[key]+distancesTwo[key])

print ("Part Two: %i" % min(combinedDistances))