
import os
from code import NPTSPSolver


TEST_PATH = "inputs/"


fout = open ("answer.out", "w")
fout.truncate() # clear file
inputs = [x for x in os.listdir(TEST_PATH) if os.path.splitext(x)[1] == '.in'] #extract inputs that end with .in
T = len(inputs) # number of test cases
for inp in inputs:
    fin = open(TEST_PATH + inp, "r")
    N = int(fin.readline()) # number of vertices
    v = [[] for i in range(N)] # 2d matrix holding vertices' edge weights
    for i in xrange(N):
        v[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline() # holds color string
    
    print('\n testing ' + str(inp))
    nptsp_solver = NPTSPSolver(N, v, c)
    mst_answer = nptsp_solver.findMST()
    #print('found my mst' + str(mst_answer))
    components = nptsp_solver.find_components(mst_answer)
    print("found my components " + str(components))
    #colorized = nptsp_solver.obey_color(components)
    #print("\n colorized my components " + str(colorized) +" \n")
    #print(str(colorized))
    #fout.write(str(sum(mst_answer))) OUTPUTS THE SUM OF THE MST EDGE WEIGHTS
    fout.write("\n")

    # find an answer, and put into assign
    #assign = [0] * N
    #for i in xrange(N):
        #assign[i] = i+1

    #fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()


