import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

#Load sample social network
#G = nx.karate_club_graph()
#G = nx.davis_southern_women_graph()
G = nx.florentine_families_graph()
pos = nx.spring_layout(G)

#Display original graph
plt.figure(1)
pos = nx.spring_layout(G)
nx.draw_networkx_edges(G,pos, alpha=0.5)
nx.draw_networkx_nodes(G, pos,node_size=400,node_color='1')
nx.draw_networkx_labels(G,pos)

#Compute the best partition
partition = community.best_partition(G,resolution=2.0)
size = float(len(set(partition.values())))
print('Number of communities: {0}'.format(int(size)))

#Clustering evaluation
print('Modularity: {0:.4f}'.format(community.modularity(partition,G)))

#Define colors of the clusters
norm = colors.Normalize(vmin=0, vmax=size, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.rainbow)

#Display partition
plt.figure(2)
pos = nx.spring_layout(G)
count = 0
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 400,
                                node_color = mapper.to_rgba(count))


nx.draw_networkx_edges(G,pos, alpha=0.5)
nx.draw_networkx_labels(G,pos)

#Calculate induced graph
ind = community.induced_graph(partition, G)

#Display induced graph
#plt.figure(3)
#pos = nx.spring_layout(ind)
#nx.draw_networkx_edges(ind,pos, alpha=0.5)
#nx.draw_networkx_nodes(ind, pos,node_size=40,node_color='1')

plt.show()

print(partition)

