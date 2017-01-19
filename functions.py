import community
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

#Functions for loading/saving objects
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

#Community functions
''' Return list of tuples with the communities and its number of members
    sorted by number of members'''
def ranking_members_community (partition,from_below=False):
    countCommunities = []
    for com in set(partition.values()):
        count = sum( x == com for x in partition.values())
        countCommunities.append([com,count])
    ranking = sorted(countCommunities, key=lambda tup: tup[1],reverse= not from_below)
    return ranking

''' Return induced graph of top N communities with more members'''
def induced_graph_ranking(G,partition,ranking,topN):
    [subG,reduced_partition] = subgraph_ranking((G,partition,ranking,topN))
    ind = community.induced_graph(reduced_partition, subG)
    return ind

''' Return sub graph and reduced partition of top N communities with more members'''
def subgraph_ranking(G,partition,ranking,topN):
    communities = [x[0] for x in ranking[0:topN]]
    reduced_partition =  { k:v for k, v in partition.items() if v in communities}
    nodes = reduced_partition.keys()
    subG = G.subgraph(nodes)
    return [subG,reduced_partition]


''' Return sub graph of a certain community'''
def subgraph_community(G,partition,community):
    nodes = list((k) for k,v in partition.items() if v == community)
    subG = G.subgraph(nodes)
    return subG

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

#Display functions
def display_partition (G,partition,figureNumber=1,edgeWidth=1,nodeSize=10):

    size = float(len(set(partition.values())))

    #Define colors of the clusters
    norm = colors.Normalize(vmin=0, vmax=size, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.rainbow)

    #Display partition
    plt.figure(figureNumber)
    pos = nx.random_layout(G)
    count = 0
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = nodeSize,
                                    node_color = mapper.to_rgba(count))
    nx.draw_networkx_edges(G,pos, alpha=0.2, width=edgeWidth)
    plt.show()
