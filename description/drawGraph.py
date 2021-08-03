import json
from sys import argv
from graphviz import Digraph

def getStructure(filename): 
    vertices = {}
    edges = []
    with open(filename, "r+", encoding='utf-8') as fd:
        for line in fd.readlines():
            if 'vertex' in line:
                _, name = line.split()
                hier = name.split(".")
                current = vertices
                for idx, elem in enumerate(hier): 
                    if idx == len(hier) - 1: 
                        if not elem in current: 
                            current[elem] = name
                    else: 
                        if (not elem in current) or isinstance(current[elem], str): 
                            current[elem] = {}
                        current = current[elem]
            elif 'edge' in line: 
                _, fromNode, toNode = line.split()
                edges.append([fromNode, toNode])
    
    return vertices, edges

def genGraph(name, vertices, edges): 
    for idx in range(len(edges)): 
        edges[idx][0] = name + "." + edges[idx][0]
        edges[idx][1] = name + "." + edges[idx][1]
    vertex2subgraph = {}
    def _genGraph(name, vertices): 
        if isinstance(vertices, dict): 
            graphName = "cluster_" + name
            graph = Digraph(graphName, engine='dot')
            graph.attr(splines = 'ortho', rankdir = 'LR')
            graph.node(name, label=name)
            vertex2subgraph[name] = graphName
            for key in vertices.keys(): 
                temp = _genGraph(name + "." + key, vertices[key])
                if isinstance(temp, str): 
                    graph.node(temp, label=key)
                    vertex2subgraph[temp] = graphName
                else: 
                    graph.subgraph(temp)
            return graph
        return name
    
    graph = _genGraph(name, vertices)
    for edge in edges: 
        graph.edge(edge[0], edge[1], ltail=vertex2subgraph[edge[0]], lhead=vertex2subgraph[edge[1]])
    return graph
        

if __name__ == "__main__": 
    filename = ""
    outputname = ""
    if len(argv) > 1:
        filename = argv[1]
    else: 
        filename = input("Filename: ")
    if len(argv) > 2:
        outputname = argv[2]
    else: 
        outputname = filename + ".dot"
    vertices, edges = getStructure(filename)
    # print(json.dumps(vertices, indent=4))
    graph = genGraph("DFG", vertices, edges)
    # graph = genGraph(filename.split("/")[-1].split(".")[0], vertices, edges)
    graph.render(outputname, view=True)
