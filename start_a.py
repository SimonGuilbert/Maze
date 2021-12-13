import gym
import car_maze as cm
from random import randrange
import time

env = cm.CarMazeEnv("open")

#################################################
# Observation space value meanings by list index:
# 0 - up       (values: 0 - road blocked,  1 - road available)
# 1 - down
# 2 - left
# 3 - right
# 4 - ID position of car
# 5 - ID position of gold
# 6 - roads / possible moves of the maze. Tuple of two ID values (from, to)
#
###########################
# Action space values
# 0 - up
# 1 - down
# 2 - left
# 3 - right

#####################################
# You code starts here
#####################################

class Node:
    def __init__(self,coordinates):
        self.coordinates = coordinates
        self.children = []
        
    def addChild(self,node):
        self.children.append(node)
        
    def getChildren(self):
        return self.children
    
    def getCoordinates(self):
        return self.coordinates
    
    def inorder(self,path):
        path.append(self.getCoordinates())
        for child in self.getChildren():
            child.inorder(path)
        return path
                     

class Graph:
    def __init__(self,root):
        self.root = root
        
    def getRandomChild(self,roads,visited):
        candidates = []
        for road in roads:
            if road[0] == self.root.getCoordinates() and road[1] not in visited:
                candidates.append(road[1])
        if not candidates:
            return None
        return Node(candidates[randrange(len(candidates))])
        
    def addStop(self,roads,visited):
        visited.append(self.root.getCoordinates())
        nextNode = self.getRandomChild(roads, visited)
        if nextNode:
            self.root.addChild(nextNode)
            Graph(nextNode).addStop(roads,visited)
            
# =============================================================================
# Outclass functions
# =============================================================================

def generateGraphs(obs,quantity):
    graphs_list = []
    start = None
    for i in range(quantity):
        while start == None or obs[5] not in start.inorder([]):
            start = Node(obs[4])
            Graph(start).addStop(obs[6], ["0-0"])
        graphs_list.append(start)
    return graphs_list

def shortPath(path,gold):
    short_path = []
    for stop in range(path.index(gold)+1):
        short_path.append(path[stop])
    return short_path

def bestPath(graphs,gold):
    best_path = shortPath(graphs[0].inorder([]),gold)
    for graph in graphs:
        path = shortPath(graph.inorder([]),gold)
        if len(path) < len(best_path):
            best_path = path
    print(best_path)
    return best_path

def getAction(starting, ending):
    x1 = int(starting.split('-')[0])
    y1 = int(starting.split('-')[1])
    x2 = int(ending.split('-')[0])
    y2 = int(ending.split('-')[1])
    if (x1 - x2) == -1:
        return 3
    if (x1 - x2) == 1:
        return 2
    if (y1 - y2) == -1:
        return 0
    if (y1 - y2) == 1:
        return 1
    
def moveCar(path):
    for t in range(len(path)-1):
        action = getAction(path[t],path[t+1])
        time.sleep(0.3)
        observation, reward, done, info = env.step(action)
        env.render()
    return reward


# =============================================================================
# Main program
# =============================================================================

# Initialisation - maze reset
first_observation = env.reset()
env.render()

# Graphs generation
quantity = 100000 # The more graphs, the more chances to find the best path
graphs = generateGraphs(first_observation,quantity)

# Best path calculation (best = shortest)
best_path = bestPath(graphs,first_observation[5])

# Actions to make the car move until the gold
reward = moveCar(best_path)
print("\nEpisode finished after",len(best_path),"timesteps")
print("Reward -",reward)


#####################################
# You code ends here
#####################################

env.close()
