

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
    def findMSTparts(self): ## CHANGED THIS FUNCTION NAME TO BE MORE APPROPRIATE -- change in NPTSP!
        mst_edges = [] # list of lists with (vertex, vertex) -- I guess we can delete this later, was just for information?
        adj_vertices = [0]*self.num_vertices
        edge_weights = []
        for index in xrange(len(self.vertices)):
            vertex = self.vertices[index]
            for weightIndex in xrange(len(vertex)):
                if index <= weightIndex:
                    weight = vertex[weightIndex]
                    if weight != 0:
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
                    adj_vertices[edge[0]-1] = [edge[1]] 
                    if adj_vertices[edge[1]-1] == 0:
                        adj_vertices[edge[1]-1] = [edge[0]]
                    else:
                        adj_vertices[edge[1]-1] += [edge[0]]
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
            else: 
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
                                    self.visited.remove(component)
                                    self.visited.remove(otherComponent)
                                    self.visited.append(component+otherComponent)
                                    visited = True
                                    if edge not in mst_edges:
                                        mst_edges.append(edge)
                                        if adj_vertices[edge[0]-1] == 0:
                                            adj_vertices[edge[0]-1] = [edge[1]] 
                                            if adj_vertices[edge[1]-1] == 0:
                                                adj_vertices[edge[1]-1] = [edge[0]]
                                            else:
                                                adj_vertices[edge[1]-1] += [edge[0]]
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
                                if adj_vertices[edge[0]-1] == 0:
                                    adj_vertices[edge[0]-1] = [edge[1]] 
                                    if adj_vertices[edge[1]-1] == 0:
                                        adj_vertices[edge[1]-1] = [edge[0]]
                                    else:
                                        adj_vertices[edge[1]-1] += [edge[0]]
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
                                    adj_vertices[edge[0]-1] = [edge[1]] 
                                    if adj_vertices[edge[1]-1] == 0:
                                        adj_vertices[edge[1]-1] = [edge[0]]
                                    else:
                                        adj_vertices[edge[1]-1] += [edge[0]]
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
                            adj_vertices[edge[0]-1] = [edge[1]] 
                            if adj_vertices[edge[1]-1] == 0:
                                adj_vertices[edge[1]-1] = [edge[0]]
                            else:
                                adj_vertices[edge[1]-1] += [edge[0]]
                        elif adj_vertices[edge[1]-1] == 0:
                            adj_vertices[edge[1]-1] = [edge[0]]
                            if adj_vertices[edge[0]-1] == 0:
                                adj_vertices[edge[0]-1] = edge[1]
                            else:
                                adj_vertices[edge[0]-1] += [edge[1]]
                        else:
                            adj_vertices[edge[0]-1] += [edge[1]]
                            adj_vertices[edge[1]-1] += [edge[0]]
        # print "EDGES"
        # print edge_weights
        # print "ADJACENCEY VERTICES"
        # print adj_vertices
        # print mst_edges

        # Breaks MST into parts now
        for k in xrange(len(adj_vertices)):
            mstedge = adj_vertices[k]
            if mstedge != 0:
                while len(mstedge) > 2:
                    lowestWeight = 101
                    lowestV = None 
                    secondLowestWeight = 101
                    secondLowestV = None 
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
                        elif weight < secondLowestWeight:
                            if secondLowestV != None:
                                adj_vertices[k].remove(secondLowestV)
                                adj_vertices[secondLowestV-1].remove(k+1)
                            secondLowestWeight = weight 
                            secondLowestV = otherV
                        else:
                            adj_vertices[k].remove(otherV)
                            adj_vertices[otherV-1].remove(k+1)
                    #adj_vertices[k] = [lowestV, secondLowestV]
        return adj_vertices
        
        # while edge_weights:
        #     curr_shortest_edge = edge_weights[0]
        #     print("current shortest")
        #     print(curr_shortest_edge)
        #     for y in range(len(vertex_list)):
        #         curr_vertex = vertex_list[y]
        #         if curr_shortest_edge in curr_vertex and self.visited[y] == 0:
        #             print("found a list, list number:")
        #             print(y)
        #             print(curr_vertex)
        #             x = curr_vertex.index(curr_shortest_edge) #the endpoint of the edge (the other vertex)
        #             mst_answer += [curr_shortest_edge]
        #             print("mst answer " + str(mst_answer))
        #             other_vertex = vertex_list[x]
        #             self.visited[x] = 1
        #             self.visited[y] = 1
        #             for i in range(self.num_vertices):
        #                 if i != y and curr_vertex[i] != -1:
        #                     edge_weights.remove(curr_vertex[i])
        #                 if i != x and other_vertex[i] != -1:
        #                     edge_weights.remove(other_vertex[i])
        #                 curr_vertex[i] = -1
        #                 other_vertex[i] = -1
        #             print("curr_vertex " + str(y) + " " + str(curr_vertex))
        #             print("other_vertex " + str(x)+ " " + str(other_vertex))
        #             break
        # print("final mst_answer returning here" + str(mst_answer))
        # return mst_answer

    """
    Returns the list of path weights that gives us a path to all the vertices.
    Stores answer in self.answer
    """
    def getAnswer():
        return nil

    def obey_color(self, components): 
        for component in components:
            if len(component) > 3:
                curr_color = "W"
                color_count = 0
                for index in range(len(component)):
                    last_color = curr_color
                    curr_color = color_str[component[index]]
                    if curr_color == last_color:
                        color_count += 1
                    else:
                        color_count = 0
                    if color_count > 3:
                        a = component[index - 3]
                        b = component[index - 2]
                        c = component[index - 1]
                        d = component[index]
                        a_b = self.vertices[a][b]
                        b_c = self.vertices[b][c]
                        c_d = self.vertices[c][d]
                        ABC = a_b + b_c
                        BCD = b_c + c_d
                        if len(component) >= (index + 1):
                            e = component[index + 1]
                            d_e = self.vertices[d][e]
                            CDE = c_d + d_e
                        if len(component) >= (index + 2):
                            f = component[index + 2]
                            if (color_str[e] == curr_color and color_str[f] == curr_color):
                                components.append(component[index:])
                                component = component[:index]
                                continue
                        if (ABC < BCD and ABC < CDE):
                            components.append(component[index:])
                            component = component[:index]
                        elif (BCD < ABC and BCD < CDE):
                            components.append(component[(index - 2):])
                            component = component[:(index - 2)]
                        else:
                            components.append(component[(index - 3):])
                            component = component[:(index - 3)]
                        continue
                        
                    #
                #
            #
        #                
        return components
