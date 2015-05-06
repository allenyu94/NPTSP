

class NPTSPSolver:

    def __init__(self, N, v, c):
        self.num_vertices = N
        self.vertices = v
        self.color_str = c
        #self.visited = [0] * N # boolean to keep track of visited vertices
        self.visited = []
        self.answer = [] # array to keep track of used edge weights
        self.last_colors = ("W", 0) # keeps track of previous colors and number of times seen

    """
    Returns list of EDGE WEIGHTS corresponding to the given vertex index i 
    """
    def getVertex(self, i):
        return self.vertices[i]
    
    """
    Returns EDGE WEIGHT corresponding to the two given vertex indices i, j
    """
    def getEdge(self, i, j):
        return self.vertices[i][j]

    """
    Updates visited list, adds path to answer. Given a path specified by 
    vertex indices i and j. Also checks validity of adding the path to the
    list.
    """
    def update(self, i, j):
        last_color = self.last_colors[0]
        last_count = self.last_colors[1]
        next_color = self.color_str[j]
        if (self.visited[j] == 1):
            print "destination vertex already visited" + str(j)
        if (self.last_colors[1] >= 3 and self.color_str[j] == last_color):
            print "visited more than 3 cities of the same color in a row"
        
        if (last_color != next_color):
            self.last_colors[0] = next_color
            self.last_colors[1] = 1
        elif (last_color == next_color):
            self.last_colors[1] += 1

    """
    Finds minimum spanning tree of inputted vertex list
    """
    def findMSTparts(self):
        mst_edges = [] # list of lists with (vertex, vertex) -- I guess we can delete this later, was just for information?
        adj_vertices = [0]*self.num_vertices
        edge_weights = []
        for index in xrange(len(self.vertices)):
            vertex = self.vertices[index]
            for weightIndex in xrange(len(vertex)):
                if index <= weightIndex:
                    weight = vertex[weightIndex]
                    if weight != 0:
                        #print([weight, vertex.index(0)+1])
                        edge_weights.append([weight, (vertex.index(0)+1, weightIndex+1)])
        
        edge_weights.sort()

        for i in xrange(len(edge_weights)):
            edge = edge_weights[i][1]
            visited = False
            # print "EDGE"
            # print edge 
            if mst_edges == []: # first edge, must add to MST
                mst_edges.append(edge)
                if adj_vertices[edge[0]-1] == 0:
                    adj_vertices[edge[0]-1] = [edge[1]] # start at index 0...
                    if adj_vertices[edge[1]-1] == 0:
                        adj_vertices[edge[1]-1] = [edge[0]]
                    else:
                        adj_vertices[edge[1]-1] += [edge[0]]
                    # print "hello"
                    # print adj_vertices
                elif adj_vertices[edge[1]-1] == 0:
                    adj_vertices[edge[1]-1] = [edge[0]]
                    if adj_vertices[edge[0]-1] == 0:
                        adj_vertices[edge[0]-1] = edge[1]
                    else:
                        adj_vertices[edge[0]-1] += [edge[1]]
                else:
                    adj_vertices[edge[0]-1] += [edge[1]]
                    adj_vertices[edge[1]-1] += [edge[0]]
                self.visited.append([edge[0],edge[1]])
                #print self.visited
            else: 
                # print "SELF VISITED"
                # print self.visited 
                for component in self.visited:
                    if edge in mst_edges: 
                        visited = True 
                    elif edge[0] in component and edge[1] in component: # THIS WOULD CREATE CYCLE
                        visited = True 
                        pass 
                    else:
                        for otherComponent in self.visited:
                            if component != otherComponent:
                                if edge[0] in component and edge[1] in otherComponent:
                                    #print "is it here?"
                                    self.visited.remove(component)
                                    self.visited.remove(otherComponent)
                                    self.visited.append(component+otherComponent)
                                    visited = True
                                    if edge not in mst_edges:
                                        mst_edges.append(edge)
                                        if adj_vertices[edge[0]-1] == 0:
                                            adj_vertices[edge[0]-1] = [edge[1]] # start at index 0...
                                            if adj_vertices[edge[1]-1] == 0:
                                                adj_vertices[edge[1]-1] = [edge[0]]
                                            else:
                                                adj_vertices[edge[1]-1] += [edge[0]]
                                            # print "hello"
                                            # print adj_vertices
                                        elif adj_vertices[edge[1]-1] == 0:
                                            adj_vertices[edge[1]-1] = [edge[0]]
                                            if adj_vertices[edge[0]-1] == 0:
                                                adj_vertices[edge[0]-1] = edge[1]
                                            else:
                                                adj_vertices[edge[0]-1] += [edge[1]]
                                        else:
                                            adj_vertices[edge[0]-1] += [edge[1]]
                                            adj_vertices[edge[1]-1] += [edge[0]]
                        if edge[0] in component: # when you have a new terminal edge to a path or something
                            component.append(edge[1])
                            visited = True
                            if edge not in mst_edges:
                                mst_edges.append(edge)
                                #print adj_vertices 
                                if adj_vertices[edge[0]-1] == 0:
                                    adj_vertices[edge[0]-1] = [edge[1]] # start at index 0...
                                    if adj_vertices[edge[1]-1] == 0:
                                        adj_vertices[edge[1]-1] = [edge[0]]
                                    else:
                                        adj_vertices[edge[1]-1] += [edge[0]]
                                    # print "hello"
                                    # print adj_vertices
                                elif adj_vertices[edge[1]-1] == 0:
                                    adj_vertices[edge[1]-1] = [edge[0]]
                                    if adj_vertices[edge[0]-1] == 0:
                                        adj_vertices[edge[0]-1] = edge[1]
                                    else:
                                        adj_vertices[edge[0]-1] += [edge[1]]
                                else:
                                    adj_vertices[edge[0]-1] += [edge[1]]
                                    adj_vertices[edge[1]-1] += [edge[0]]
                        elif edge[1] in component:
                            component.append(edge[0])
                            visited = True 
                            if edge not in mst_edges:
                                mst_edges.append(edge)
                                if adj_vertices[edge[0]-1] == 0:
                                    adj_vertices[edge[0]-1] = [edge[1]] # start at index 0...
                                    if adj_vertices[edge[1]-1] == 0:
                                        adj_vertices[edge[1]-1] = [edge[0]]
                                    else:
                                        adj_vertices[edge[1]-1] += [edge[0]]
                                    # print "hello"
                                    # print adj_vertices
                                elif adj_vertices[edge[1]-1] == 0:
                                    adj_vertices[edge[1]-1] = [edge[0]]
                                    if adj_vertices[edge[0]-1] == 0:
                                        adj_vertices[edge[0]-1] = edge[1]
                                    else:
                                        adj_vertices[edge[0]-1] += [edge[1]]
                                else:
                                    adj_vertices[edge[0]-1] += [edge[1]]
                                    adj_vertices[edge[1]-1] += [edge[0]]
                if visited == False:
                    self.visited.append([edge[0], edge[1]])
                    if edge not in mst_edges:
                        mst_edges.append(edge)
                        if adj_vertices[edge[0]-1] == 0:
                            adj_vertices[edge[0]-1] = [edge[1]] # start at index 0...
                            if adj_vertices[edge[1]-1] == 0:
                                adj_vertices[edge[1]-1] = [edge[0]]
                            else:
                                adj_vertices[edge[1]-1] += [edge[0]]
                            # print "hello"
                            # print adj_vertices
                        elif adj_vertices[edge[1]-1] == 0:
                            adj_vertices[edge[1]-1] = [edge[0]]
                            if adj_vertices[edge[0]-1] == 0:
                                adj_vertices[edge[0]-1] = edge[1]
                            else:
                                adj_vertices[edge[0]-1] += [edge[1]]
                        else:
                            adj_vertices[edge[0]-1] += [edge[1]]
                            adj_vertices[edge[1]-1] += [edge[0]]
                # print "SELF VISITED AFTER"
                # print visited
                # print self.visited
                # check that self.visited only has one item in list?
        # print "EDGes"
        # print edge_weights
        # print "ADJACENCEY VERTICES"
        # print adj_vertices
        # print mst_edges

        #print self.vertices

        for k in xrange(len(adj_vertices)):
            mstedge = adj_vertices[k]
            if mstedge != 0:
                # print mstedge 
                # print len(mstedge)
                while len(mstedge) > 2:
                    #print "too long"
                    lowestWeight = 101
                    lowestV = None 
                    secondLowestWeight = 101
                    secondLowestV = None 
                    #edgesToKeep = [] #?
                    for otherV in mstedge:
                        weight = self.vertices[k][otherV-1]
                        if weight < lowestWeight:
                            if secondLowestV != None:
                                adj_vertices[k].remove(secondLowestV)
                                adj_vertices[secondLowestV-1].remove(k+1)
                            if lowestV != None:
                                adj_vertices[k].remove(lowestV)
                                adj_vertices[lowestV-1].remove(k+1)
                            secondLowestWeight = lowestWeight
                            secondLowestWeightV = lowestV
                            lowestWeight = weight 
                            lowestV = otherV
                            # if edgesToKeep == []:
                            #     edgesToKeep.append(otherV)
                            # else:
                            #     edgesToKeep = [otherV, edgesToKeep[0]]
                        elif weight < secondLowestWeight:
                            if secondLowestV != None:
                                adj_vertices[k].remove(secondLowestV)
                                adj_vertices[secondLowestV-1].remove(k+1)
                            secondLowestWeight = weight 
                            secondLowestV = otherV

                            #edgesToKeep = [edgesToKeep[0], otherV]
                        else:
                            # print adj_vertices
                            # print k 
                            # print otherV 
                            # print mstedge 
                            adj_vertices[k].remove(otherV)
                            adj_vertices[otherV-1].remove(k+1)
                    #adj_vertices[k] = [lowestV, secondLowestV]
        print adj_vertices





    """
    Returns the list of path weights that gives us a path to all the vertices.
    Stores answer in self.answer
    """
    def getAnswer():
        return nil


    #def obey_color(self, components):