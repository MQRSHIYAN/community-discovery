import community
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import pickle

############## CONFIGURATION ##############
dataset = 1
load_partition=True
display_plots=False
###########################################

#Load sample social network
if dataset == 1:
    G = nx.read_edgelist('DBLP_graph.txt')
elif dataset == 2:
    G = nx.read_edgelist('soc-flickr.mtx')
else:
    print('A valid dataset number was not provided')
    exit()

#Print information of dataset
print ('Number of nodes: ', nx.number_of_nodes(G))
print ('Number of edges: ', nx.number_of_edges(G))

#Example datasets
#G = nx.karate_club_graph()
#G = nx.davis_southern_women_graph()
#G = nx.florentine_families_graph()

if display_plots:
    #Configure layout
    pos = nx.random_layout(G)

    #Display original graph
    plt.figure(1)
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    nx.draw_networkx_nodes(G, pos,node_size=10,node_color='1')

    plt.show()

if load_partition:
    #Load partition from file
    partition = load_obj('partition_dataset_' + str(dataset))
else:
    #Compute the best partition
    partition = community.best_partition(G)
    size = float(len(set(partition.values())))
    print('Number of communities: {0}'.format(int(size)))

    #Save partition in file
    save_obj(partition, 'partition_dataset_' + str(dataset))

#Clustering evaluation
print('Modularity: {0:.4f}'.format(community.modularity(partition,G)))

if display_plots:
    #Define colors of the clusters
    norm = colors.Normalize(vmin=0, vmax=size, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.rainbow)

    #Display partition
    plt.figure(2)
    pos = nx.random_layout(G)
    count = 0
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 10,
                                    node_color = mapper.to_rgba(count))


    nx.draw_networkx_edges(G,pos, alpha=0.5)
    plt.show()

#Calculate induced graph
#ind = community.induced_graph(partition, G)

#Display induced graph
#if display_plots:
#   plt.figure(3)
#   pos = nx.spring_layout(ind)
#   nx.draw_networkx_edges(ind,pos, alpha=0.5)
#   nx.draw_networkx_nodes(ind, pos,node_size=40,node_color='1')
#   plt.show()

#Get Opinion Leaders(OP)
opinion_leaders(20)

#Function for saving objects
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

##Role functions

''' Return list of tuples with the top N opinion leaders and their score'''
def opinion_leaders (G,topN):
    scores = nx.pagerank(G)
    ranking = sorted(scores, key=scores.get,reverse=True)
    if (topN > len(scores)): topN = len(scores)
    topRanking=[]
    for i in range(0,topN):
        topRanking.append([ranking[i],scores[str(ranking[i])]])
    return topRanking
