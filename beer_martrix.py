import pandas as pd
import numpy as np
from tabulate import tabulate
from itertools import combinations

b_dir = '../instacart/order_products__prior.csv/'
b1_dir = '../instacart/products.csv/'

df = pd.read_csv(b_dir + 'order_products__prior.csv')
df_product = pd.read_csv(b1_dir + 'products.csv')
dic = df_product.set_index('product_id')['product_name'].to_dict()


def f(df, col1, col2):
    keys, values = df[[col1, col2]].sort_values(col1).values.T
    ukeys, index = np.unique(keys, True)
    arrays = np.split(values, index[1:])
    df2 = pd.DataFrame({col1: ukeys, col2: [list(a) for a in arrays]})
    return df2


df_cart = f(df, 'order_id', 'product_id')


def get_product_set(name):
    return set(df_product[df_product['product_name'].str.lower(
    ).str.contains(name)]['product_id'].tolist())


diaper_set = get_product_set('beer')


def get_dic_node_edge(df, tag_list_col):
    dic_edge = {}
    dic_node = {}
    for tag_list in df[tag_list_col]:
        if len(diaper_set.intersection(set(tag_list))) > 0:
            tag_list = sorted(tag_list)
            for source, target in combinations(tag_list, 2):
                dic_edge.setdefault((source, target), 0)
                dic_edge[(source, target)] += 1
            for node in tag_list:
                dic_node.setdefault(node, 0)
                dic_node[node] += 1
    return (dic_node, dic_edge)


dic_node, dic_edge = get_dic_node_edge(df_cart, 'product_id')
sorted_edge_list = sorted(
    dic_edge.items(), key=lambda item: item[1], reverse=True)
import pickle as pk
with open('dic_node.pickle', 'wb') as f:
    pk.dump(dic_node, f)

with open('dic_edge.pickle', 'wb') as f:
    pk.dump(dic_edge, f)

with open('sorted_edge_4000000.pickle', 'wb') as f:
    pk.dump(sorted_edge_list[:4000000], f)
