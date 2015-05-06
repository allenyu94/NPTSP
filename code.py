
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
        checklist = [x for x in self.vertices]
        master_list = []
        for vlist in self.vertices:
            master_list += vlist
        master_list.sort()

        count = 0
        # remove zero weights for edges to itself
        while count != self.num_vertices:
            master_list.remove(0)
            count += 1

        while master_list:
            curr_shortest = master_list[0]
            print("current shortest")
            print(curr_shortest)
            for y in range(len(checklist)):
                currlist = checklist[y]
                if curr_shortest in currlist and self.visited[y] == 0:
                    print("found a list, list number:")
                    print(y)
                    print(currlist)
                    x = currlist.index(curr_shortest)
                    mst_answer += [curr_shortest]
                    print("mst answer")
                    print(mst_answer)
                    otherlist = checklist[x]
                    self.visited[x] = 1
                    self.visited[y] = 1
                    for i in range(self.num_vertices):
                        if i != y and currlist[i] != -1:
                            master_list.remove(currlist[i])
                        if i != x and otherlist[i] != -1:
                            master_list.remove(otherlist[i])
                        currlist[i] = -1
                        otherlist[i] = -1
                    break
        return mst_answer

    """
    Returns the list of path weights that gives us a path to all the vertices.
    Stores answer in self.answer
    """
    def getAnswer():
        return nil
