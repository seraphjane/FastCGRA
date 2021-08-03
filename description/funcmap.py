from networkx.algorithms.operators.unary import reverse
import xmltodict
import json
import networkx as nx
from networkx.algorithms import isomorphism as iso

import utils
from utils import Base
from protocols import *

class IsoMapper(Base): 
    def __init__(self, graph, units): 
        self._original = graph
        self._units    = units
        self._patterns = {}
        self._matched  = []
        self._map      = {}
        self._graph    = Graph()
        self._compat   = {}

    def match(self): 
        for uname, unit in self._units.items(): 
            self._patterns[uname] = {}
            for pname, patt in unit.patterns().items(): 
                self._patterns[uname][pname] = patt.graph()
                # print("Pattern: " + uname + "." + pname)
                # print(self._patterns[uname][pname].info())
                # print("Matching: " + uname + "." + pname)
                g1 = self._original.toNX()
                g2 = self._patterns[uname][pname].toNX()
                matcher = iso.DiGraphMatcher(g1, g2, lambda x, y: x["attrs"]["function"] == y["attrs"]["function"])
                # print(matcher.subgraph_is_isomorphic())
                isomorphisms = matcher.subgraph_isomorphisms_iter()
                for match in isomorphisms: 
                    self._matched.append((uname, pname, match, ))
                    # print(match)
        self._matched.sort(key=lambda x: (len(x[2]), -len(self._units[x[0]].patterns())), reverse=True)
        # print(self._original.info())
        # print(utils.list2str(self._matched))
        
        used = set()
        for match in self._matched: 
            uname = match[0]
            pname = match[1]
            info  = match[2]
            duplicated = False
            for v1, v2 in info.items(): 
                if v1 in used: 
                    duplicated = True
                    break
            if duplicated: 
                continue
            for v1, v2 in info.items(): 
                used.add(v1)

            vertexName = ""
            for v1, v2 in info.items(): 
                if not "." in v1: 
                    vertexName += v1 + "_"
            vertexName = vertexName[:-1]
            self._graph.addVertex(vertexName, {"unit": uname, "pattern": pname})
            if not vertexName in self._compat: 
                self._compat[vertexName] = set()
            self._compat[vertexName].add(uname)
            for v1, v2 in info.items(): 
                portName = ""
                portType = ""
                for key, value in self._units[uname].pattern(pname).portMap().items(): 
                    if value == v2: 
                        portName = key
                        if portName in self._units[uname].inputs(): 
                            portType = "input"
                        elif portName in self._units[uname].outputs(): 
                            portType = "output"
                        else: 
                            assert portName in self._units[uname].inputs() or portName in self._units[uname].outputs(), "IsoMapper: Invalid port: " + portName + " of " + uname
                if portName != "": 
                    temp = portName
                    portName = vertexName + "." + portName
                    self._graph.addVertex(portName, {"unit": uname + "." + temp})
                    self._map[v1] = portName
                    if portType == "input": 
                        self._graph.addEdge(portName, vertexName, {})
                    elif portType == "output": 
                        self._graph.addEdge(vertexName, portName, {})
        # print(utils.dict2str(self._map))

        if len(used) < len(self._original.vertices()): 
            print("IsoMapper: FAILED. ")
            exit(1) 

        for vname, vertex in self._original.vertices().items(): 
            if vname in self._map: 
                for edge in self._original.edgesOut()[vname]: 
                    if edge.to() in self._map: 
                        self._graph.addEdge(self._map[edge.fr()], self._map[edge.to()], {})

    def graph(self): 
        return self._graph

    def graphInfo(self): 
        return self._graph.info()

    def compat(self): 
        return self._compat

    def compatInfo(self): 
        info = ""
        for vertex, compats in self._compat.items(): 
            info += vertex
            for compat in compats: 
                info += " " + compat
            info += "\n"
        return info

def trivial(ops, units): 
    result = ""
    for opname in ops: 
        op = ops[opname]
        optype = op.type()
        found = False
        mapped = []
        for key in units: 
            unit = units[key]
            funcs = unit.funcs()
            for name in funcs: 
                func = funcs[name]
                if func[0:2] == "__": 
                    func = func[2:]
                if func[-2:] == "__": 
                    func = func[:-2]
                if func == optype: 
                    found = True
                    mapped.append(unit.name())
        temp = opname
        for unit in mapped: 
            temp += " " + unit
        result += temp + "\n"
        # print("Map " + opname + " to " + utils.list2str(mapped))
    return result
    




#TODO
