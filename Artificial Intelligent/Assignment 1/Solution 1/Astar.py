# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 04:50:59 2019

@author: ashima
"""

import numpy as np

from min_heap import Heap
from AstarNode import Node
#from utils import convert_tostring, convert_tostate, find_successors, isCompleted
from utils import find_successors, isCompleted

def manhattan_dist(origpos, statepos):
    dist = np.abs(origpos[0][0] - statepos[0][0]) + np.abs(origpos[1][0] - statepos[1][0])
    return dist

#H Val = “Total Number of misplaced tiles to goal positions in board n”    
def calHeuristic1(state, goal, M, N):
    count = 0
    for i in range(M):
        for j in range(N):
            if state[i][j] != goal[i][j]:
                count += 1
    return count

#Hval = “sum of distances of misplaced tiles to goal positions in board n”
def calHeuristic2(state, goal, M, N):
    dist = 0
    #print(goal_string)
    for i in range(M):
        for j in range(N):
            a = goal[i][j]
            origpos = np.where(goal == a)
            statepos = np.where(state == a)
            if origpos != statepos:
                dist += manhattan_dist(origpos, statepos)
    return dist

def Astar(start, goal, M, N):
    #Declare min heap of capacity 100
    priority_queue = Heap(10000)
    exploredSet = []
    #state_string = convert_tostring(start, M, N)
    #goal_string = convert_tostring(goal, M, N)
    #Take heuristic value to be maximum of the two heuristic functions
    heuristicf = max(calHeuristic1(start, goal, M, N), calHeuristic2(start, goal, M, N))
    startNode = Node(start, "NoParent", 0, heuristicf)
    priority_queue.addNode(startNode)
    while priority_queue:
        s = priority_queue.delNode()
        state = s.state
        if isCompleted(state, goal, M, N):
            return "Solved"
        exploredSet.append(state)
        #state = convert_tostate(state, M, N)
        successors = find_successors(state, M, N)
        for i in successors:
            if any(np.array_equal(elem, i) for elem in exploredSet):
                continue
            #heuristicf = calHeuristic2(start, goal, goal_string)
            heuristicf = max(calHeuristic1(state, goal, M, N), calHeuristic2(state, goal, M, N))
            startNode = Node(i, state, (s.get_g() + 1), heuristicf)
            priority_queue.addNode(startNode)
    

if __name__ == "__main__":
    M, N = 3, 3
    goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', 'E']]
    start = [['1', '2', '3'], ['4', '5', '6'], ['7', 'E', '8']]
#    M, N = 4, 4
#    goal = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', 'E']]
#    start = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', 'E', '11'], ['13', '14', '15', '12']]
    ans = Astar(np.asarray(start), np.asarray(goal), M, N)
    print(ans)