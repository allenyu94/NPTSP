
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
    def findMST(self):
        mst_edges = [] # list of lists with (vertex, vertex)
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
        #print(edge_weights)
        for i in xrange(len(edge_weights)):
            edge = edge_weights[i][1]
            visited = False
            # print "EDGE"
            # print edge 
            if mst_edges == []: # first edge, must add to MST
                mst_edges.append(edge)
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
                        if edge[0] in component: # when you have a new terminal edge to a path or something
                            component.append(edge[1])
                            visited = True
                            if edge not in mst_edges:
                                mst_edges.append(edge)
                        elif edge[1] in component:
                            component.append(edge[0])
                            visited = True 
                            if edge not in mst_edges:
                                mst_edges.append(edge)
                if visited == False:
                    self.visited.append([edge[0], edge[1]])
                    if edge not in mst_edges:
                        mst_edges.append(edge)
                # print "SELF VISITED AFTER"
                # print visited
                # print self.visited
                # check that self.visited only has one item in list?
        print mst_edges


    """
    Returns the list of path weights that gives us a path to all the vertices.
    Stores answer in self.answer
    """
    def getAnswer():
        return nil


    #def obey_color(self, components):