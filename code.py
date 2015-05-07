

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
        mst_edges = [] 
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
            # print self.visited 
            # print mst_edges
            if mst_edges == []: # first edge, must add to MST
                mst_edges.append(edge)
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
        adj_vertices = [0]*self.num_vertices
        for e in mst_edges:
            v1 = e[0]
            v2 = e[1]
            if adj_vertices[v1-1] == 0:
                adj_vertices[v1-1] = [v2-1]
            else:
                adj_vertices[v1-1] += [v2-1]
            if adj_vertices[v2-1] == 0:
                adj_vertices[v2-1] = [v1-1]
            else:
                adj_vertices[v2-1] += [v1-1]
        return adj_vertices

    """
    Takes an MST and returns the paths between each component.  A component
    consists of nodes and edges that make a path, and all components together
    gives you the path separated by edges.

    The MST is represented by an adjacency list.
    """
    def find_components(self, mst):
        
	adj_list = mst
        path_components = [] 
	start = None

	#print "Starting to find path components"

	while self.remains(adj_list):
	    #print "In the while loop"
	    #print "This is adj_list: " + str(adj_list)
	    for i in range(self.num_vertices):
	        if len(adj_list[i]) == 1:
		    start = i
		    break
	    #print "We start here: " + str(start)
            one_component = self.components(adj_list, start, [start])
	    path_components.append(one_component)
	    for vertex in one_component:
		for i in range(self.num_vertices):
		    if vertex in adj_list[i]: 
		        if len(adj_list[i]) == 1 and not self.multiconnected(adj_list, i):
			    path_components.append([i])
		        adj_list[i].remove(vertex)
		adj_list[vertex] = []
	
	#print "These are path components: " + str(path_components)
	return path_components

    """
    Find whether a vertex is only connected to the graph by one edge.
    """
    def multiconnected(self, list, v):
	count = 0
	for vlist in list:
	    if v in vlist:
	        count += 1
        if count > 1:
	    return True
	return False


    """
    Helper method to find_components to count the number of edges in the MST
    that have yet to be considered.
    """
    def remains(self, alist):
        #print "Checking remains"
        count = 0
        for edge_list in alist:
	    if not edge_list:
	        #print edge_list
		#print "Found empty list"
	        count += 1
	if count == self.num_vertices:
	    #jprint "no more edges to consider"
	    return False 
	#print "** Not done yet! **"
	return True 

    """
    A recursive helper method which takes the current adjacency list, the 
    current vertex (denoted as index), as well as the list of the component 
    so far.

    Each call will find the smallest [remaining] edge incident on the current
    vertex and choose it to be part of the component.
    """
    def components(self, list, index, current_list):

        if not list[index]:
	    #print "The list before the end: " + str(list)
	    return current_list

	minm = 101
	next_index = None
	for v in list[index]:
	    if self.vertices[index][v] < minm:
	        minm = self.vertices[index][v]
		next_index = v
	#print "The next vertex is: " + str(v)
	#print "This next list is: " + str(list[next_index])
	#print "The current index is: " + str(index)
	#print "The current list is: " + str(list[index])
	list[index].remove(next_index)
	list[next_index].remove(index)
	current_list += [next_index]
	return self.components(list, next_index, current_list)


    def update_info(path_list):

        info_list = [None] * self.num_vertices
        
	for path in path_list:
	    start = path[0]
	    end = path[-1]
	    start_color = self.color_str[start]
	    end_color = self.color_str[end]

	    continuous = 1



    """
    Returns the list of path weights that gives us a path to all the vertices.
    Stores answer in self.answer
    """
    def getAnswer():
        return nil

    def obey_color(self, components): 
        for comp_index in xrange(len(components)):
            component = components[comp_index]
            #print(component)
            if len(component) > 3:
                curr_color = "W"
                color_count = 0
                for index in range(len(component)):
                    last_color = curr_color
                    curr_color = self.color_str[component[index]]
                    #print("\n last_color is " + last_color)
                    #print("curr_color is " + curr_color + "\n")
                    if curr_color == last_color:
                        color_count += 1
                    else:
                        color_count = 0
                    if color_count >= 3:
                        #print("got into more than 3 of the same color count, index is " + str(index))
                        a = component[index - 3]
                        b = component[index - 2]
                        c = component[index - 1]
                        d = component[index]
                        #print ("a = %d, b = %d, c = %d, d = %d" % (a, b, c, d))
                        a_b = self.vertices[a][b]
                        b_c = self.vertices[b][c]
                        c_d = self.vertices[c][d]
                        ABC = a_b + b_c
                        BCD = b_c + c_d
                        if len(component) > (index + 1):
                            e = component[index + 1]
                            #print("e = %d" % (e))
                            d_e = self.vertices[d][e]
                            CDE = c_d + d_e
                        if len(component) > (index + 2):
                            f = component[index + 2]
                            if (color_str[e] == curr_color and color_str[f] == curr_color):
                                components.append(component[index:])
                                components[comp_index] = component[:index]
                                break 
                        if (ABC < BCD and ABC < CDE):
                            components.append(component[index:])
                            components[comp_index] = component[:index]
                        elif (BCD < ABC and BCD < CDE):
                            components.append(component[(index - 2):])
                            components[comp_index] = component[:(index - 2)]
                        else:
                            components.append(component[(index - 1):])
                            components[comp_index] = component[:(index - 1)]
                        break
                        
                    #
                #
            #
        #                
        return components
