
class NPTSPSolver:

    def __init__(self, N, v, c):
        self.num_vertices = N
        self.vertices = v
        self.color_str = c
        self.visited = [0] * N # boolean to keep track of visited vertices
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
        mst_answer = []
        vertex_list = [x for x in self.vertices]
        edge_weights = []
        for vertex in self.vertices:
            edge_weights += vertex
        print (edge_weights)
        edge_weights.sort()

        count = 0
        # remove zero weights for edges to itself
        while count != self.num_vertices:
            edge_weights.remove(0)
            count += 1

        while edge_weights:
            curr_shortest_edge = edge_weights[0]
            print("current shortest")
            print(curr_shortest_edge)
            for y in range(len(vertex_list)):
                curr_vertex = vertex_list[y]
                if curr_shortest_edge in curr_vertex and self.visited[y] == 0:
                    print("found a list, list number:")
                    print(y)
                    print(curr_vertex)
                    x = curr_vertex.index(curr_shortest_edge)
                    mst_answer += [curr_shortest_edge]
                    print("mst answer")
                    print(mst_answer)
                    other_vertex = vertex_list[x]
                    self.visited[x] = 1
                    self.visited[y] = 1
                    for i in range(self.num_vertices):
                        if i != y and curr_vertex[i] != -1:
                            edge_weights.remove(curr_vertex[i])
                        if i != x and other_vertex[i] != -1:
                            edge_weights.remove(other_vertex[i])
                        curr_vertex[i] = -1
                        other_vertex[i] = -1
                    break
        return mst_answer

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

	while self.remains(adj_list):
	    for i in range(self.num_vertices):
	        if len(adj_list[i]) == 1:
		    start = i
		    break
	    path_components.append(self.component(adj_list, start, [start]))

	return path_components


    """
    Helper method to find_components to count the number of edges in the MST
    that have yet to be considered.
    """
    def remains(self, alist):
        count = 0
        for edge_list in alist:
	    if not edge_list:
	        count += 1
	return count == self.num_vertices

    """
    A recursive helper method which takes the current adjacency list, the 
    current vertex (denoted as index), as well as the list of the component 
    so far.

    Each call will find the smallest [remaining] edge incident on the current
    vertex and choose it to be part of the component.
    """
    def components(self, list, index, current_list):

        if not list:
	    return current_list

	minm = 101
	next_index = None
	for v in list[index]:
	    if self.vertices[index][v] < minm:
	        minm = self.vertices[index][v]
		next_index = v
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


    #def obey_color(self, components):
