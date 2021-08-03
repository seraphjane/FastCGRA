import utils
from utils import Base
import networkx as nx

class Vertex(Base): 
    def __init__(self, name, attrs = {}): 
        self._name  = name
        self._attrs = attrs.copy()

    def name(self): 
        return self._name

    def attrs(self): 
        return self._attrs

    def attr(self, name): 
        return self._attrs[name] if name in self._attrs else None

    def copy(self): 
        return Vertex(self._name, self._attrs)

    def info(self): 
        return "Vertex: " + self._name + "; Attributes: " + utils.dict2str(self._attrs) + "."

class Edge(Base): 
    def __init__(self, fr, to, attrs = {}): 
        self._fr    = fr
        self._to    = to
        self._attrs = attrs.copy()

    def fr(self): 
        return self._fr

    def to(self): 
        return self._to

    def attrs(self): 
        return self._attrs

    def attr(self, name): 
        return self._attrs[name] if name in self._attrs else None

    def copy(self): 
        return Edge(self._fr, self._to, self._attrs)

    def info(self): 
        return "Edge: " + self._fr + " -> " + self._to + "; Attributes: " + utils.dict2str(self._attrs) + "."

class Graph(Base): 
    def __init__(self): 
        self._vertices = {}
        self._edgesIn  = {}
        self._edgesOut = {}
    
    def vertex(self, name): 
        return self._vertices[name] if name in self._vertices else None
    
    def vertices(self): 
        return self._vertices
    
    def edgesIn(self, name = ""): 
        if len(name) == 0: 
            return self._edgesIn
        return self._edgesIn[name] if name in self._edgesIn else None
    
    def edgesOut(self, name = ""): 
        if len(name) == 0: 
            return self._edgesOut
        return self._edgesOut[name] if name in self._edgesOut else None

    def addVertex(self, name, attrs = {}): 
        self._vertices[name] = Vertex(name, attrs)
        if not name in self._edgesIn: 
            self._edgesIn[name] = []
        if not name in self._edgesOut: 
            self._edgesOut[name] = []

    def addEdge(self, fr, to, attrs = {}): 
        assert fr in self._vertices, "Graph: Invalid edge source: " + fr
        assert to in self._vertices, "Graph: Invalid edge sink: " + to
        self._edgesIn[to].append(Edge(fr, to, attrs))
        self._edgesOut[fr].append(Edge(fr, to, attrs))

    def parse(self, info): 
        lines = info.split("\n")
        index = 0
        while index < len(lines): 
            line = lines[index]
            splited = line.split()
            if len(splited) > 1 and splited[0] == "vertex": 
                name  = splited[1]
                attrs = {}
                temp = index + 1
                tempSplited = lines[temp].split() if temp < len(lines) else []
                while len(tempSplited) == 0 or lines[temp][0] == "#" or tempSplited[0] == "attr": 
                    if temp >= len(lines): 
                        break
                    if len(tempSplited) == 0 or lines[temp][0] == "#": 
                        temp += 1
                        tempSplited = lines[temp].split() if temp < len(lines) else []
                        continue
                    if tempSplited[0] == "attr": 
                        attrName  = tempSplited[1]
                        attrType  = tempSplited[2]
                        attrValue = tempSplited[3]
                        if attrType == "int": 
                            attrValue = int(attrValue)
                        attrs[attrName] = attrValue
                    temp += 1
                    tempSplited = lines[temp].split() if temp < len(lines) else []
                self.addVertex(name, attrs)
                index = temp
            if len(line) > 4 and line[0:4] == "edge": 
                fr, to = splited[1:3]
                attrs = {}
                temp = index + 1
                tempSplited = lines[temp].split() if temp < len(lines) else []
                while len(tempSplited) == 0 or lines[temp][0] == "#" or tempSplited[0] == "attr": 
                    if temp >= len(lines): 
                        break
                    if len(tempSplited) == 0 or lines[temp][0] == "#": 
                        temp += 1
                        tempSplited = lines[temp].split() if temp < len(lines) else []
                        continue
                    if tempSplited[0] == "attr": 
                        attrName  = tempSplited[1]
                        attrType  = tempSplited[2]
                        attrValue = tempSplited[3]
                        if attrType == "int": 
                            attrValue = int(attrValue)
                        attrs[attrName] = attrValue
                    temp += 1
                    tempSplited = lines[temp].split() if temp < len(lines) else []
                self.addEdge(fr, to, attrs)
                index = temp

    def copy(self): 
        newgraph = Graph()
        newgraph._vertices = {}
        newgraph._edgesIn  = {}
        newgraph._edgesOut = {}
        for name in self._vertices: 
            newgraph._vertices[name] = self._vertices[name].copy()
            newgraph._edgesIn[name] = []
            newgraph._edgesOut[name] = []
            for edge in self._edgesIn[name]: 
                newgraph._edgesIn[name].append(edge.copy())
            for edge in self._edgesOut[name]: 
                newgraph._edgesOut[name].append(edge.copy())
        return newgraph

    def info(self, prefix = ""): 
        result = ""
        for name in self._vertices: 
            vertex = self._vertices[name]
            result += "vertex " + vertex.name() + "\n"
            for nameAttr in vertex.attrs(): 
                result += "attr " + nameAttr + " " + ("str " if isinstance(vertex.attr(nameAttr), str) else "int ") + vertex.attr(nameAttr) + "\n"
        for vertex in self._vertices: 
            assert vertex in self._edgesOut, "Graph: Invalid edge source: " + vertex
            for edge in self._edgesOut[vertex]: 
                result += "edge " + edge.fr() + " " + edge.to() + "\n"
                for nameAttr in edge.attrs(): 
                    result += "attr " + nameAttr + " " + ("str " if isinstance(edge.attr(nameAttr), str) else "int ") + edge.attr(nameAttr) + "\n"
        return result

    def prefixed(self, prefix = ""): 
        def addPrefix(name): 
            if len(prefix) == 0: 
                return name
            return prefix + "." + name
        newgraph = Graph()
        for name in self._vertices: 
            namePrefixed = addPrefix(name)
            newgraph._vertices[namePrefixed] = self._vertices[name].copy()
            newgraph._vertices[namePrefixed]._name = namePrefixed
            newgraph._edgesIn[namePrefixed] = []
            newgraph._edgesOut[namePrefixed] = []
        for name in self._vertices: 
            assert name in self._edgesOut, "Graph: Invalid edge source: " + name 
            namePrefixed = addPrefix(name)
            for idx in range(len(self._edgesIn[name])): 
                newgraph._edgesIn[namePrefixed].append(Edge(addPrefix(self._edgesIn[name][idx]._fr), addPrefix(self._edgesIn[name][idx]._to), self._edgesIn[name][idx]._attrs))
            for idx in range(len(self._edgesOut[name])): 
                newgraph._edgesOut[namePrefixed].append(Edge(addPrefix(self._edgesOut[name][idx]._fr), addPrefix(self._edgesOut[name][idx]._to), self._edgesOut[name][idx]._attrs))
        return newgraph
    
    def extend(self, graph): 
        for key in graph.vertices(): 
            if not key in self._vertices: 
                self._vertices[key] = graph.vertices()[key].copy()
                self._edgesIn[key]  = []
                self._edgesOut[key] = []
            else: 
                print("Graph: Warning: duplicated vertex " + key + ": ignored")
        for key in graph.vertices(): 
            for edge in graph.edgesIn(key): 
                self._edgesIn[key].append(edge.copy())
            for edge in graph.edgesOut(key): 
                self._edgesOut[key].append(edge.copy())

    def toNX(self): 
        g = nx.DiGraph()
        for vname, vertex in self._vertices.items(): 
            g.add_node(vname, attrs=vertex.attrs())
        for vname, edges in self._edgesOut.items(): 
            for edge in edges: 
                g.add_edge(edge.fr(), edge.to())
        return g


        
