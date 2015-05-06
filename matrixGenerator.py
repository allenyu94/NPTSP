import fileinput

first = True 
matrix = None 
for line in fileinput.input():

	if first:
		first = False 
		matrix =  [[100]*int(line) for i in range(int(line))]  #[[100]*int(line)]*int(line) # can change the default of the other lines you don't care about
		for j in xrange(int(line)):
			matrix[j][j] = 0
	else:
		line = line.split()
		edge = line[0]
		weight = line[1]
		matrix[int(edge[1])-1][int(edge[3])-1] = weight 
		matrix[int(edge[3])-1][int(edge[1])-1] = weight 

# print out 
for row in matrix:
	for elem in row:
		print elem,
	print('\n')


