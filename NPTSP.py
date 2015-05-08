
import os
from code import NPTSPSolver


TEST_PATH = "instances/"


fout = open ("answer.out", "w")
fout.truncate() # clear file
inputs = [x for x in os.listdir(TEST_PATH) if os.path.splitext(x)[1] == '.in'] #extract inputs that end with .in
T = len(inputs) # number of test cases
#for inp in inputs:
for inp in [5]:
    #fin = open(TEST_PATH + inp, "r")
    fin = open(TEST_PATH + str(inp+1) + ".in", "r")
    N = int(fin.readline()) # number of vertices
    v = [[] for i in range(N)] # 2d matrix holding vertices' edge weights
    for i in xrange(N):
        v[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline() # holds color string
    
    print('\n testing ' + str(inp+1))
    nptsp_solver = NPTSPSolver(N, v, c)
    
    mst_answer = nptsp_solver.findMST()
    #print('found my mst' + str(mst_answer))
    
    components = nptsp_solver.find_components(mst_answer)
    #print("found my components " + str(components))
    
    colorized = nptsp_solver.obey_color(components)
    #print("\n colorized my components " + str(colorized) +" \n")

    info_list = nptsp_solver.update_info(colorized)
    #print("\n the color and number of consecutive color nodes info: " + str(info_list) + "\n")
    
    combined_comp = nptsp_solver.combine(colorized, info_list)
    if not combined_comp:
        combined_comp = []
    print("\n the combined component: " + str(combined_comp) + "\n")
    
    answer = nptsp_solver.getAnswer(combined_comp)
    print("\n total weight is: " + str(answer[1]) + "\n")
    #fout.write(str(sum(mst_answer))) OUTPUTS THE SUM OF THE MST EDGE WEIGHTS
    fout.write(" ".join(str(x) for x in combined_comp))
    fout.write("\n")

    # find an answer, and put into assign
    #assign = [0] * N
    #for i in xrange(N):
        #assign[i] = i+1

    #fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()
