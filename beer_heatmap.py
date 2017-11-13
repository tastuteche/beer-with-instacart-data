import pandas as pd
import numpy as np
b1_dir = '../instacart/products.csv/'

df_product = pd.read_csv(b1_dir + 'products.csv')
dic = df_product.set_index('product_id')['product_name'].to_dict()


import pickle as pk
with open('dic_node.pickle', 'rb') as f:
    dic_node = pk.load(f)

with open('sorted_edge_4000000.pickle', 'rb') as f:
    sorted_edge_4000000 = pk.load(f)

top_N = 100
top_N_node = set()
for (source, target), weight in sorted_edge_4000000[:top_N]:
    top_N_node.add(source)
    top_N_node.add(target)
dic_top_N = {}
for node in top_N_node:
    dic_top_N[node] = dic_node[node]
sorted_node_list = sorted(
    dic_top_N.items(), key=lambda item: item[1], reverse=True)

top_N_node_list = [item[0] for item in sorted_node_list]


import networkx as nx
G = nx.Graph()
for (source, target), weight in sorted_edge_4000000[:top_N]:
    G.add_node(source, node_size=dic_node[source])
    G.add_node(target, node_size=dic_node[target])
    G.add_edge(source, target, weight=weight)

#matrix = nx.adjacency_matrix(G, nodelist=top_N_node_list, weight='weight')
matrix = nx.to_numpy_matrix(G, nodelist=top_N_node_list, weight='weight')
import matplotlib.pyplot as plt

# il me semble que c'est une bonne habitude de faire supbplots
fig, axis = plt.subplots()
# heatmap contient les valeurs
heatmap = axis.pcolor(np.array(matrix), cmap=plt.cm.Blues)

axis.set_yticks(np.arange(matrix.shape[0]) + 0.5, minor=False)
axis.set_xticks(np.arange(matrix.shape[1]) + 0.5, minor=False)

# axis.invert_yaxis()

row_labels = [dic[n] for n in top_N_node_list]
col_labels = [dic[n] for n in top_N_node_list]
fontdict = {'fontsize': 7}
axis.set_yticklabels(row_labels, fontdict=fontdict, minor=False)
axis.set_xticklabels(col_labels, fontdict=fontdict, rotation=270, minor=False)

fig.set_size_inches(15, 15)
plt.colorbar(heatmap)
# plt.show()
plt.savefig('heatmap.png', dpi=200)
from tabulate import tabulate

pair_list, count_list = zip(*sorted_edge_4000000[:top_N])
pair_a_list, pair_b_list = zip(*pair_list)
df_top_N = pd.DataFrame(list(zip([dic[a] for a in pair_a_list], [
                        dic[b] for b in pair_b_list], count_list)), columns=['product1', 'product2', 'count'])

with open('df_top_N.txt', 'w') as f:
    f.write(tabulate(df_top_N, tablefmt="pipe", headers="keys"))
