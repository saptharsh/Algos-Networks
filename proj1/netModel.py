'''
Created on Jun 24, 2016

@author: smart
'''
import matplotlib.pyplot as plot
import pygraphviz as pygv
import networkx as ntx
import random

def getcost(N, k):
    tup = [[] for i in range(N)]
    tup1 = [[] for i in range(N)]
    
for i in range(N):
    a = [[i, j, 1] for j in range(N) if j != i else 0]
    b = [1 if j != i else 0 for j in range(N)]
    ran = random.sample(list(filter(lambda x:x != i, range(N - 1))), k)
    
for j in ran:
    a[j][2] = 300
    b[j] = 300
    tup[i] = a
    tup1[i] = b
    tup = [tup[i][j] if i != j for i in range(N) for j in range(N)]
    return (tup, tup1)

def function(N, k):
    cost = getcost(N, k)
    cost_matrix = cost[1]
    # print cost_matrix
    graph = ntx.DiGraph()
    graph.add_nodes_from(range(N))

    graph.add_weighted_edges_from(cost[0])
    # to calculate the Bij values of the network
    myid = '2021209213'
    repl = myid * 3
    # formulae used to calculate the Bij values
    bijvalues = [[abs(int(repl[q]) - int(repl[p]))
                  for p in range(N)] for q in range(N)]
    link_capacity = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j & bijvalues[i][j] != 0:
                repl = ntx.dijkstra_path(g, i, j)
                path = [(repl[x], repl[x + 1]) for x in range(len(repl) - 1)]
                for m in path:
                    link_capacity[m[0]][m[1]] = link_capacity[m[0]][m[1]] + bijvalues[i][j]
                    # setting the vars with initial values
                    optimal_cost = 0
                    num_edges = 0
                    for i in range(N):
                        for j in range(N):
                            if link_capacity[i][j] != 0:
                                num_edges = num_edges + 1
                                optimal_cost += cost_matrix[i][j] * link_capacity[i][j]
                                # Calculating the density using the given formulae
                                density = num_edges / float(N * (N - 1))

                                kplots = [3, 9, 15]
                                if k in kplots:
                                    kGraph = pygv.AGraph(strict=False, directed=True)
                                    kGraph.graph_attr.update(size="10,10")
                                    kGraph.add_nodes_from(range(N))
                                    for i in range(N):
                                        for j in range(N):
                                            if i != j & link_capacity[i][j] != 0:
                                                kGraph.add_edge(i, j, label=link_capacity[i][j])
                                                kGraph.draw('file-' + str(k) + '.ps', prog='circo')
                                                return
                                            {'optimal_cost':optimal_cost, 'density':density}
                                            
def main():
    optimal_cost = []
    density = []
    N = 30
    # K values ranging from 3 to 16
    for i in range(3, 16):
        result = function(N, i)
        optimal_cost.append(result['optimal_cost'])
        density.append(result['density'])
        print ("optimal cost when k =", i, ":", result['optimal_cost'], ", density", result['density'])
        # Plotting graph showing changes in the cost with K
        k = range(3, 16)
        plot.plot(k, optimal_cost)


        plot.xlabel('k')
        plot.ylabel('Total cost')
        plot.title('Total cost vs k')
        plot.show()
        # Plotting graph showing changes in the density with K
        plot.plot(k, density)
        plot.xlabel('k')
        plot.ylabel('Density')
        plot.title('Density vs k')
        plot.show()
        
main()
