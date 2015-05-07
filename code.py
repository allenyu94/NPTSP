

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
        return self.edges[i]
    
    """
    Returns EDGE WEIGHT corresponding to the two given vertex indices i, j
    """
    def getEdge(self, i, j):
        return self.edges[i][j]

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
            # print "MY CURRENT MST"
            # print mst_edges
            if mst_edges == []: # first edge, must add to MST
                mst_edges.append(edge)
                self.visited.append([edge[0],edge[1]])
            else: 
                self.MSThelper(edge, mst_edges, visited)
                
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
        # print "MY MSTTTT"
        # print mst_edges 
        return adj_vertices

    def MSThelper(self, edge, mst_edges, visited):
        for component in self.visited:
            if edge in mst_edges: 
                #visited = True 
                return 
            elif edge[0] in component and edge[1] in component: # THIS WOULD CREATE CYCLE
                #visited = True 
                #pass 
                return 
            else:
                for otherComponent in self.visited:
                    if component != otherComponent:
                        if (edge[0] in component and edge[1] in otherComponent):# or (edge[1] in component and edge[0] in otherComponent):
                            # print "WHYYY"
                            # print edge[0]
                            # print edge[1]
                            # print component 
                            # print otherComponent 
                            self.visited.remove(component)
                            # print "after"
                            # print self.visited
                            self.visited.remove(otherComponent)
                            self.visited.append(component+otherComponent)
                            #visited = True

                            if edge not in mst_edges:
                                mst_edges.append(edge)
                            return 
        for component in self.visited:
            if edge[0] in component: # when you have a new terminal edge to a path or something
                component.append(edge[1])
                
                if edge not in mst_edges:
                    mst_edges.append(edge)
                return 
            elif edge[1] in component:
                component.append(edge[0])
                
                if edge not in mst_edges:
                    mst_edges.append(edge)
                return 
        #if visited == False:
        self.visited.append([edge[0], edge[1]])
        if edge not in mst_edges:
            mst_edges.append(edge)
        return 

    """
    Takes an MST and returns the paths between each component.  A component
    consists of nodes and edges that make a path, and all components together
    gives you the path separated by edges.

    The MST is represented by an adjacency list.
    """
    def find_components(self, mst):
        
	adj_list = mst
        path_components = [] 

	while self.remains(adj_list):
	    start = None
	    min_val = 101
	    for i in range(self.num_vertices):
	        if len(adj_list[i]) == 1:
		    vertex = adj_list[i][0]
		    if self.vertices[i][vertex] < min_val:
		        min_val = self.vertices[i][vertex]
		        start = i
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

    """
    Helper method that will determine the color of the terminal nodes on each
    path and how many nodes of the same color have been seen before it

    path_list is a list of path components that have been correctly colored
    and will output a list of tuples, where the ith position will contain 
    information if and only if the ith node is a terminal node in some path,
    otherwise it contains None.
    """
    def update_info(self, path_list):

        info_list = [None] * self.num_vertices
        
        for path in path_list:
            start = path[0]
            end = path[-1]
            start_color = self.color_str[start]
            end_color = self.color_str[end]

            continuous = 1

            #If the path is a singleton, assign the color and continous = 1
            if len(path) == 1:
                info_list[start] = (start_color, continuous)

                #If the path is just a pair of nodes, check if the colors match
            #and assign continuous accordingly.
            elif len(path) == 2:
                if start_color == end_color:
                    info_list[start] = (start_color, continuous + 1)
                    info_list[end] = (end_color, continuous + 1)
                else:
                    info_list[start] = (start_color, continuous)
                    info_list[end] = (end_color, continuous)

            else: 
                second = path[1]
                third = path[2]
                second_color = self.color_str[second]
                third_color = self.color_str[third]
                
                if start_color == second_color and start_color == third_color:
                    info_list[start] = (start_color, continuous + 2)
                elif start_color == second_color:
                    info_list[start] = (start_color, continuous + 1)
                else:
                    info_list[start] = (start_color, continuous)

                second_last = path[-2]
                third_last = path[-3]
                before_last = self.color_str[second_last]
                thirdToLast = self.color_str[third_last]

                if end_color == before_last and end_color == thirdToLast:
                    info_list[end] = (end_color, continuous + 2)
                elif end_color == before_last:
                    info_list[end] = (end_color, continuous + 1)
                else:
                    info_list[end] = (end_color, continuous)

        return info_list

    """
    Input: a list of components where each component is a list of vertices
    Output: a list of components where each component is now guaranteed to follow the coloring rule
    
    1) For each component check if there is a potential for coloring issues (if theres more than 3 vertices).
    2) If yes, then traverse through the component until you find 4 of the same color in a row.
    3) Check if there's 6 of the same color in a row: if yes, break it so its 3 | 3
    4) Check ABC < BCD.
    5) If there's 5 of the same color in a row, further check if CDE < whichever is smaller from above.
    6) Splice the component accordingly: splicing the component currently being proecessed and adding the leftover back into the list of comonents.
    """
    def obey_color(self, components): 
        color_str = self.color_str
        for comp_index in xrange(len(components)):
            component = components[comp_index]
            #print(component)
            if len(component) > 3:
                curr_color = "W"
                color_count = 0
                for index in range(len(component)):
                    last_color = curr_color
                    curr_color = color_str[component[index]]
                    #print("\n last_color is " + last_color)
                    #print("curr_color is " + curr_color + "\n")
                    if curr_color == last_color:
                        color_count += 1
                    else:
                        color_count = 0
                    if color_count >= 3:
                        #if there's 6 in a row of the same color, evenly divide it
                        if len(component) > (index + 2):
                            if (color_str[component[index + 1]] == curr_color and color_str[component[index + 2]] == curr_color):
                                components.append(component[index:])
                                components[comp_index] = component[:index]
                                break 

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
                        
                        e = -1
                        if len(component) > (index + 1):
                            e = component[index + 1]
                            #print("e = %d" % (e))
                            d_e = self.vertices[d][e]
                            CDE = c_d + d_e
                            
                        if ABC < BCD:
                            if e != -1:
                                if CDE < ABC:
                                    components.append(component[(index - 1):])
                                    components[comp_index] = component[:(index - 1)]
                                    break
                            components.append(component[index:])
                            components[comp_index] = component[:index]
                            break
                            
                        else:
                            if e != -1:
                                if CDE < BCD:
                                    components.append(component[(index - 1):])
                                    components[comp_index] = component[:(index - 1)]
                                    break
                            components.append(component[(index - 2):])
                            components[comp_index] = component[:(index - 2)]
                            break
        return components

        """
    Update info array if vertex is an endpoint of a component. Specify how many of the same color is adjacent to this vertex.
    """
    def updateInfo(self, components):
        # set color string manually
        self.color_str = "RRBBRRBB"
        print self.color_str 

        info = [0]*self.num_vertices
        for component in components:
            size = len(component)
            if size == 1:
                if info[component[0]] == 0:
                    info[component[0]] = self.color_str[component[0]]
        print info


    """
    Gets the component that contains a certain vertex index
    """
    def getcomponent(self, components, vertex):
        for comp in components:
            if vertex in comp:
                return comp

    """
    Repositions component if necessary to maintain consistency
    of the start and end of the list to be endpoints of components.
    Inputs first comp, start endpoint, other comp, and other endpoint.
    Ensures that two endpoints are combined in middle of the two lists.

    (start endpoint) [first comp] + [other comp] (end endpoint)
    this func. flips both comps and combines

    [first comp] (start endpoint) + [other comp] (end endpoint)
    this func. flips second comp and combines

    """
    def combineComponents(self, firstcomp, s_point, othercomp, e_point):
        if firstcomp[0] == s_point: 
            # start point is in front of first comp
            firstcomp = firstcomp[::-1]
        if othercomp[0] == e_point:
            # end point is in front of other comp
            othercomp = othercomp[::-1]
        return firstcomp + othercomp

    """
    Removes the component containing the vertex and returns the new
    updated components list
    """
    def removeComponent(self, components, vertex):
        for index in xrange(len(components)):
            comp = components[index]
            if vertex in comp:
                components.remove(comp)
                return components


    """
    Combines the components and related info to create the NPTSP path
    """
    def combine(self, components, info):
        #print "my components: " + str(components) + "\n"
        #print "my info: " + str(info) + "\n"
        while len(components) != 1: # while I still don't have a single path
            first_index = None
            for index in xrange(len(info)):
                info_entry = info[index]
                if info_entry:
                    print("\ncurr vertex is " + info_entry[0] + ", %d.  This is vertex number %d \n" % (info_entry[1], index))
                    first_index = index
                    startcomp = self.getcomponent(components, index)
                    shortest_edge = 200
                    closest_comp_index = None
                    for info_index in xrange(len(info)):
                        next_endpoint = info[info_index]
                        if info_index == index:
                            pass
                        elif next_endpoint == None or len(next_endpoint) == 0:
                            pass
                        # else: 
                            # if info[info_index]:
                        else:
                            #print("this time info[info_index] is " + str(info[info_index]))
                            currcolor = info_entry[0]
                            curr_num = info_entry[1]
                            varcolor = next_endpoint[0]
                            varnum = next_endpoint[1]
                            #print "curr color: " + str(currcolor)
                            #print "curr num: " + str(curr_num)
                            #print "var color: " + str(varcolor)
                            #print "var num: " + str(varnum)
                            print ("next color is " + varcolor + ", %d.  This is vertex number %d"  %  (varnum, info_index))
                            if currcolor != varcolor or (currcolor == varcolor and curr_num + varnum <= 3):
                                # if valid coloring
                                if self.vertices[index][info_index] < shortest_edge: 
                                    # if the new comp is closest so far
                                    shortest_edge = self.vertices[index][info_index]
                                    closest_comp_index = info_index
                                        #
                                #
                            # if not info[info_index]:
                            #     # empty info section: continue
                            #     continue
                            # currcolor = info_entry[0]
                            # curr_num = info_entry[1]
                            # varcolor = info[info_index][0]
                            # varnum = info[info_index][1]
                            # #print "curr color: " + str(currcolor)
                            # #print "curr num: " + str(curr_num)
                            # #print "var color: " + str(varcolor)
                            # #print "var num: " + str(varnum)
                            # if currcolor != varcolor or (currcolor == varcolor and curr_num + varnum <= 3):
                            #     # if valid coloring
                            #     if self.vertices[index][info_index] < shortest_edge: 
                            #         # if the new comp is closest so far
                            #         shortest_edge = self.vertices[index][info_index]
                            #         closest_comp_index = info_index
                            #     #
                            # #
                        #
                    print("%d got matched with %d" % (index, closest_comp_index))
                    if not closest_comp_index:
                        # if there is no valid path
                        print("no closest component!")
                        return None
                    # updating info
                    info[first_index] = []
                    info[closest_comp_index] = []
                    # updating components
                    #print "components before edit: " + str(components)
                    othercomp = self.getcomponent(components, closest_comp_index)
                    #print ("old comp: " + str(startcomp))
                    #print ("old comp: " + str(othercomp))
                    newcomp = self.combineComponents(startcomp, first_index, othercomp, closest_comp_index)
                    #print "new comp: " + str(newcomp)
                    components = self.removeComponent(components, first_index)
                    components = self.removeComponent(components, closest_comp_index)
                    components.append(newcomp)
                    #print "components after edit: " + str(components)
                    break
        return components[0] 


    """
    Returns the path list and total weight of the entire path as a tuple
    ([path], total weight)
    """
    def getAnswer(self, path):
        if path:
            return (path, sum(path))
        else:
            return (None, 0)

