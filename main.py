import community
import networkx as nx
import matplotlib.pyplot as plt

#Load sample social network
G = nx.karate_club_graph()
pos = nx.spring_layout(G)

#Display original graph
plt.figure(1)
pos = nx.spring_layout(G)
nx.draw_networkx_edges(G,pos, alpha=0.5)
nx.draw_networkx_nodes(G, pos,node_size=20,node_color='0')

#Compute the best partition
partition = community.best_partition(G)

#Display partition
plt.figure(2)
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    print(count)
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
