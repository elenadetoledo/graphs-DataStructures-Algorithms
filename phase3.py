from graph import AdjacentVertex
from graph import Graph

import math
import queue

class Graph2(Graph):
    def min_number_edges(self, start: str, end: str) -> int: #apply a BFS
        """returns the minimum number of edges from start to end"""
        visited = [] #nodes analyzed are stored here
        distances = [] #here will be stored the distances from the start to each possible node
        q = queue.Queue() #create a queue
        count = -1
        for i in self._vertices.keys(): #go through all nodes
            count += 1
            distances.append(math.inf) #set initial values of the list to infinity
            if i == start:
                distances[count] = 0
            if i == end:
                endpos = count #this will be position in distances list

        q.put(start) #insert first element in the queue. BFS algorithm
        results = self._min_number_edges(visited,distances,q) #call recursive function
        min = results[endpos] #check the distance in the wanted position
        if min == math.inf: #no possible path
            results[endpos] = 0
        return results[endpos]

    def _min_number_edges(self,visited:list,distances:list,q:queue):
        if q.empty():
            return distances #list with the distances from the start to each node
        else:
            counter = -1
            x = q.get() #obtain the first element in the queue
            if x not in visited: #if we already analyzed it, ignore
                visited.append(x) #analyze it and add to visited
                for i in self._vertices[x]: #go through adjacents
                    if i.vertex not in visited:
                        q.put(i.vertex) #add to queue
                        for j in self._vertices.keys(): #through all nodes
                            counter += 1
                            if j == x:
                                pos = counter
                            if j == i.vertex:
                                adj = counter
                        counter = -1
                        lastd = distances[adj]
                        newd = distances[pos]+ 1
                        if newd < lastd: #if the new distance calculated to reach such node is less than the previous one then update it, a different path has reached it with less edges
                            distances[adj] = newd
                        else:
                            distances[adj] = lastd

            return self._min_number_edges(visited,distances,q) #recursive function with an updated queue


    def transpose(self) -> 'Graph2':
        """ returns a new graph that is the transpose graph of self"""
        if self._directed: #if it is undirected there transpose can not be computed
            if len(self._vertices.keys()) == 0:
                return None #empty list
            trans = Graph2(self._vertices.keys(),True) #create a copy of the given graph
            for i in self._vertices.keys(): #go through each node
                for j in self._vertices[i]: #check its adjacents
                    trans.add_edge(j.vertex,i) #create an edge in the opposite direction in the new graph
            return trans
        else: #in the case it is undirected the transpose is itself
            return self



    def is_strongly_connected(self):
        """This function checks if the graph is strongly connected.
        A directed graph is strongly connected when for any
        pair of vertices u and v, there is always a path from u to v.
        If the graph is undirected, the function returns True if the graph is
        connected, that is, there is a path from any vertex to any other vertex
        in the graph."""
        boolean = True
        for i in self._vertices.keys(): #for all the nodes check if there exists a path with any other node of the graph
            for j in self._vertices.keys():
                if i != j: #because simple graph
                    result = self.checkconnection(i, j) #auiliary function to check connections
                    if result == False:
                        boolean = False

        return boolean


    def checkconnection(self,a, b):
        visited=[] #create a visited list to prevent infinite loops
        result= self._checkconnection(a, b, visited) #call the recursive function
        if result==0:
            return False
        if result==1:
            return True
        
    def _checkconnection(self,vert1, vert2, visited):
        result=0
        if vert1 not in visited: #if is in visited, does not analyze the possible path
            visited.append(vert1) #it it was not visited append it to the list since we are going to analyze the possible path
            for i in self._vertices[vert1]: #check if one of their adjacents is the goal node
                if i.vertex not in visited:
                    if i.vertex == vert2: #if its adjacent is the goal, them a possible path is accomplished
                        result=1 #path encountered and break the loop
                        break
                    else: #if the goal is not adjacent, check if there exists a possible path from any of their adjacents
                        result=self._checkconnection(i.vertex, vert2, visited)
                        if result==1:
                            break
        return result