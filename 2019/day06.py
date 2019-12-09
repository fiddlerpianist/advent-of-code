from anytree import Node, RenderTree

def findOrCreate(name, dict):
    if name not in dict:
        dict[name] = Node(name, parent=None)
    return dict[name]

nodesDict = {}
edges = 0

# build the tree
with open('day06.txt') as f:
    for line in f:
        orbit = line.rstrip().split(")")
        parentName = orbit[0]
        childName = orbit[1]
        parentNode = findOrCreate(parentName, nodesDict)
        childNode = findOrCreate(childName, nodesDict)
        childNode.parent = parentNode

# Part One
for i in nodesDict:
    #print (nodesDict[i])
    edges += nodesDict[i].depth

print ("Part One: %i" % edges)

"""for pre, fill, node in RenderTree(nodesDict["COM"]):
    print("%s%s" % (pre, node.name))
"""

def stepsToSanta(cursor, santa, steps):
    if santa in cursor.descendants:
      # the last steps are the difference between where we are and where Santa is
        steps += santa.depth - cursor.depth
        return steps - 2
    elif santa in cursor.ancestors:
        steps += cursor.depth - santa.depth
        return steps - 2
    else:
        return stepsToSanta(cursor.parent, santa, steps + 1)

steps = stepsToSanta(nodesDict["YOU"], nodesDict["SAN"], 0)
print ("Part Two: %s" % steps)

 
