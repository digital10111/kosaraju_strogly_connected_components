# kosaraju_strogly_connected_components

import operator
import sys
sys.setrecursionlimit(100000)
explored = set()
t = 0
node_s = None
f = {}
leader = {}
finished = []


class DGraph:
    def __init__(self, vertices, edges_list, edges_endpoint_dict, vertices_to_outgoing_edges):
        self.vertices = vertices
        self.edges_list = edges_list
        self.edges_endpoint_dict = edges_endpoint_dict
        self.vertices_to_outgoing_edges = vertices_to_outgoing_edges

def dfs_loop_first_pass(graph_G):
    global explored
    global node_s
    node_s = None
    for node_i in reversed(graph_G.vertices):
        if node_i not in explored:
            node_s = node_i
            dfs_first_pass_iter(graph_G, node_i)

def dfs_first_pass_iter(graph_G, node_i):
    global explored
    global t
    global node_s
    global f
    global leader
    global finished
    stack = list()
    unfinished_stack = list()
    stack.append(node_i)

    while stack:
        vertex = stack.pop()
        if vertex not in explored:
            explored.add(vertex)
            if vertex not in graph_G.vertices_to_outgoing_edges:
                continue
            for arc in graph_G.vertices_to_outgoing_edges[vertex]:
                node_j = graph_G.edges_endpoint_dict[arc][1]
                if node_j not in explored:
                    stack.append(node_j)
                    if vertex not in unfinished_stack:
                        unfinished_stack.append(vertex)
                elif vertex not in f:
                    t = t + 1
                    f[vertex] = t
                    if vertex in unfinished_stack:
                        unfinished_stack.remove(vertex)
    while unfinished_stack:
        this_vertex = unfinished_stack.pop()
        t = t + 1
        f[this_vertex] = t

def dfs_second_pass_iter(graph_G, node_i, f_node_i):
    global explored
    global node_s
    global f
    global leader

    stack = list()
    stack.append(node_i)
    while stack:
        vertex = stack.pop()
        if f[vertex] not in explored:
            explored.add(f[vertex])
            if vertex not in leader:
                leader[vertex] = node_s
            if vertex not in graph_G.vertices_to_outgoing_edges:
                continue
            for arc in graph_G.vertices_to_outgoing_edges[vertex]:
                node_j = graph_G.edges_endpoint_dict[arc][1]

                f_node_j = f[node_j]
                if f_node_j not in explored:
                    stack.append(node_j)
                    explored.add(f[vertex])
                    leader[node_j] = node_s

def dfs_loop_second_pass(graph_G, sorted_fin_times):
    global explored
    explored = set()
    global leader
    leader = {}
    global node_s
    global f

    for (node_i, fin_time) in reversed(sorted_fin_times):
        if f[node_i] not in explored:
            node_s = node_i
            dfs_second_pass_iter(graph_G, node_i, f[node_i])

if __name__ == '__main__':
    file_path = "GRAPH.txt"
    vertices = [i for i in range(1, 875715)]

    edges_list = []
    edges_endpoint_dict = {}
    edges_endpoint_dict_rev = {}

    vertices_to_outgoing_edges = {}
    vertices_to_outgoing_edges_rev = {}

    with open(file_path, 'r') as edges_:
        for i, edge in enumerate(edges_):
            edges_list.append(i + 1)
            v1 = int(edge.split(' ')[0])
            v2 = int(edge.split(' ')[1])
            edges_endpoint_dict[i+1] = (v1, v2)
            edges_endpoint_dict_rev[i+1] = (v2, v1)
            if v1 not in vertices_to_outgoing_edges:
                vertices_to_outgoing_edges[v1] = list()
            if v2 not in vertices_to_outgoing_edges_rev:
                vertices_to_outgoing_edges_rev[v2] = list()
            vertices_to_outgoing_edges[v1].append(i + 1)
            vertices_to_outgoing_edges_rev[v2].append(i + 1)

    graph_rev = DGraph(vertices, edges_list, edges_endpoint_dict_rev, vertices_to_outgoing_edges_rev)
    graph = DGraph(vertices, edges_list, edges_endpoint_dict, vertices_to_outgoing_edges)

    dfs_loop_first_pass(graph_rev)
    fin_time_sorted = [(k, f[k]) for k in f.keys()]
    fin_time_sorted.sort(key=operator.itemgetter(1))
    print fin_time_sorted
    dfs_loop_second_pass(graph, fin_time_sorted)
    import json
    json.dump(leader, open('leader.txt', 'w'))
    
    
    
    
# def dfs(graph_G, node_i):
#     global explored
#     global node_s
#     global f
#     explored.add(node_i)
#     if node_i in graph_G.vertices_to_outgoing_edges:
#         for arc in graph_G.vertices_to_outgoing_edges[node_i]:
#             node_j = graph_G.edges_endpoint_dict[arc][1]
#             if node_j not in explored:
#                 dfs(graph_G, node_j)

#     global t
#     t = t + 1
#     f[node_i] = t
#     return f



# def dfs_second_pass(graph_G, node_i, f_node_i):
#     global explored
#     global node_s
#     global f
#     global leader
#     explored.add(f_node_i)
#     leader[node_i] = node_s
#     if node_i in graph_G.vertices_to_outgoing_edges:
#         for arc in graph_G.vertices_to_outgoing_edges[node_i]:
#             node_j = graph_G.edges_endpoint_dict[arc][1]
#             f_node_j = f[node_j]
#             if f_node_j not in explored:
#                 dfs_second_pass(graph_G, node_j, f_node_j)
