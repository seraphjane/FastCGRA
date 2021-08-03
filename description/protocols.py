import utils
from utils import Base
from graph import Graph

class Function(Base): 
    def __init__(self, name, info = {}): 
        if len(info) == 0: 
            info = {"input": [], "output": [], "width": "32"}
        if not "input" in info: 
            info["input"] = []
        if not "output" in info: 
            info["output"] = []
        if not "width" in info: 
            info["width"] = 32
        self._name    = name
        self._inputs  = info["input"].copy()
        self._outputs = info["output"].copy()
        self._width   = int(info["width"])
    
    def name(self): 
        return self._name

    def inputs(self): 
        return self._inputs

    def outputs(self): 
        return self._outputs

    def input(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._inputs[index]
    
    def output(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._outputs[index]

    def width(self): 
        return self._width

    def info(self): 
        return "Function Name: "    + self._name + "\t -> " + \
               "Inputs: "  + utils.list2str(self._inputs) + "; " + \
               "Outputs: " + utils.list2str(self._outputs) + "; " + \
               "Width: "   + str(self._width) + "."

class Pattern(Base): 
    def __init__(self, name, info = {}): 
        if len(info) == 0: 
            info = {"unit": [], "port": {}, "connection": []}
        if not "unit" in info: 
            info["unit"] = []
        if not "port" in info: 
            info["port"] = {}
        if not "connection" in info: 
            info["connection"] = []
        self._name    = name
        self._units   = info["unit"].copy()
        self._portMap = info["port"].copy()
        self._conns   = info["connection"].copy()
        self._graph   = Graph()
    
    def name(self): 
        return self._name
    
    def units(self): 
        return self._units
    
    def portMap(self): 
        return self._portMap
    
    def graph(self): 
        return self._graph

    def construct(self, funcsLocal, funcsGlobal): 
        for vertex in self._units: 
            function = funcsLocal[vertex]
            self._graph.addVertex(vertex, {"function": function, })
            assert function in funcsGlobal, "Pattern: Invalid function: " + function
            for inport in funcsGlobal[function].inputs(): 
                name = vertex + "." + inport
                self._graph.addVertex(name, {"function": function + "." + inport, })
                self._graph.addEdge(name, vertex, {})
            for outport in funcsGlobal[function].outputs(): 
                name = vertex + "." + outport
                self._graph.addVertex(name, {"function": function + "." + outport, }) 
                self._graph.addEdge(vertex, name, {})
        for conn in self._conns: 
            splited = conn.split("->")
            assert len(splited) == 2, "Pattern: Invalid connection: " + conn
            fr, to = splited
            assert fr in self._graph.vertices(), "Pattern: Invalid edge source: " + fr
            assert to in self._graph.vertices(), "Pattern: Invalid edge sink: " + to
            self._graph.addEdge(fr, to, {})

    def info(self): 
        return "Pattern Name: " + self._name + "\n"\
               " -> Port Relation: " + utils.dict2str(self._portMap) + "\n" + \
               " -> Pattern Graph: " + "\n\t".join([""] + self._graph.info().split("\n"))


class Unit(Base): 
    def __init__(self, name, info = {}): 
        if len(info) == 0: 
            info = {"input": [], "output": [], "function": {}, "pattern": {}, "compat": {}, }
        if not "input" in info: 
            info["input"] = []
        if not "output" in info: 
            info["output"] = []
        if not "function" in info: 
            info["function"] = {}
        if not "pattern" in info: 
            info["pattern"] = {}
        if not "compat" in info: 
            info["compat"] = {}
        self._name      = name
        self._inputs    = info["input"].copy()
        self._outputs   = info["output"].copy()
        self._functions = info["function"].copy()
        self._patterns  = {}
        for name in info["pattern"]: 
            pattern = Pattern(name, info["pattern"][name])
            self._patterns[name] = pattern
        self._compats = info["compat"].copy()
    
    def name(self): 
        return self._name

    def inputs(self): 
        return self._inputs

    def outputs(self): 
        return self._outputs

    def input(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._inputs[index]
    
    def output(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._outputs[index]

    def funcs(self): 
        return self._functions

    def func(self, name): 
        if not name in self._functions: 
            return None
        return self._functions[name]

    def patterns(self): 
        return self._patterns

    def pattern(self, name): 
        if not name in self._patterns: 
            return None
        return self._patterns[name]

    def compats(self): 
        return self._compats

    def compat(self, name): 
        if not name in self._compats: 
            return None
        return self._compats[name]

    def construct(self, funcsGlobal): 
        for key in self._patterns.keys(): 
            self._patterns[key].construct(self._functions, funcsGlobal)

    def info(self): 
        result = "Unit Name: \t" + self._name + "\n" + \
                 " -> Input Ports: \t" + utils.list2str(self._inputs) + "\n" + \
                 " -> Output Ports: \t" + utils.list2str(self._outputs) + "\n" + \
                 " -> Patterns: "
        for key in self._patterns: 
            result += "\n\t".join([""] + self._patterns[key].info().split("\n"))
        result += "\n -> Compatible Patterns: " + "\n\t".join(utils.dict2str(self._compats).split("\n"))
        return result


class Switch(Base): 
    def __init__(self, name, info = {}): 
        if len(info) == 0: 
            info = {"input": [], "output": [], "required": [], "graph": ""}
        if not "input" in info: 
            info["input"] = []
        if not "output" in info: 
            info["output"] = []
        if not "required" in info: 
            info["required"] = []
        if not "graph" in info: 
            info["graph"] = ""
        self._name      = name
        self._inputs    = info["input"].copy()
        self._outputs   = info["output"].copy()
        self._required  = info["required"].copy()
        self._graphAbs  = Graph()
        self._graphInfo = info["graph"]
        self._graph     = Graph()
        for name in self._inputs: 
            self._graphAbs.addVertex(name, {"type": "__MODULE_INPUT_PORT__", "device": self._name + "." + name})
        for name in self._outputs: 
            self._graphAbs.addVertex(name, {"type": "__MODULE_OUTPUT_PORT__", "device": self._name + "." + name})
        for conn in self._required: 
            splited = conn.split("->")
            assert len(splited) == 2
            fr, to = splited
            assert fr in self._graphAbs.vertices(), "Switch: Invalid edge source: " + fr
            assert to in self._graphAbs.vertices(), "Switch: Invalid edge sink: " + to
            self._graphAbs.addEdge(fr, to, {})
        #TODO: self._graph

    def inputs(self): 
        return self._inputs

    def outputs(self): 
        return self._outputs

    def input(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._inputs[index]
    
    def output(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._outputs[index]

    def required(self): 
        return self._required

    def graphAbs(self): 
        return self._graphAbs

    def info(self): 
        return "Switch Name: " + self._name + "\n" + \
               " -> Switch Graph: " + "\n\t".join([""] + self._graphAbs.info().split("\n"))

class Module(Base): 
    def __init__(self, name, info = {}): 
        if len(info) == 0: 
            info = {"input": [], "output": [], "required": [], }
        self._name        = name
        self._inputs      = info["input"].copy()
        self._outputs     = info["output"].copy()
        self._modules     = info["module"].copy()
        self._elements    = info["element"].copy()
        self._switches    = info["switch"].copy()
        self._connections = []
        for conn in info["connection"]: 
            splited = conn.split("->")
            assert len(splited) == 2
            self._connections.append(splited)
        self._graphAbs    = Graph()
        self._fus         = {}

    def inputs(self): 
        return self._inputs

    def outputs(self): 
        return self._outputs

    def input(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._inputs[index]
    
    def output(self, index): 
        if index >= len(self._inputs): 
            return None
        return self._outputs[index]

    def modules(self): 
        return self._modules

    def elements(self): 
        return self._elements

    def switches(self): 
        return self._switches

    def connections(self): 
        return self._connections

    def graphAbs(self): 
        return self._graphAbs

    def fus(self): 
        return self._fus

    def construct(self, units, switches, modules): 
        for inport in self._inputs: 
            self._graphAbs.addVertex(inport, {"type": "__MODULE_INPUT_PORT__", "device": self._name + "." + inport, })
        for outport in self._outputs: 
            self._graphAbs.addVertex(outport, {"type": "__MODULE_OUTPUT_PORT__", "device": self._name + "." + outport, })
        for key in self._elements: 
            typeUnit = self._elements[key]
            assert typeUnit, "Module: Invalid unit: (" + key + ", " + typeUnit + ")"
            self._graphAbs.addVertex(key, {"type": typeUnit, "device": typeUnit, "unit": typeUnit, })
            assert not key in self._fus, "Module: FU duplicated: " + key
            self._fus[key] = {"type": typeUnit, "device": typeUnit, "inputs": units[typeUnit].inputs(), "outputs": units[typeUnit].outputs()}
            for inport in units[typeUnit].inputs(): 
                self._graphAbs.addVertex(key + "." + inport, {"type": "__ELEMENT_INPUT_PORT__", "device": typeUnit + "." + inport, })
                self._graphAbs.addEdge(key + "." + inport, key, {})
            for outport in units[typeUnit].outputs(): 
                self._graphAbs.addVertex(key + "." + outport, {"type": "__ELEMENT_OUTPUT_PORT__", "device": typeUnit + "." + outport, })
                self._graphAbs.addEdge(key, key + "." + outport, {})
        for key in self._switches: 
            typeSwitch = self._switches[key]
            assert typeSwitch in switches, "Module: Invalid switch: (" + key + ", " + typeSwitch + ")"
            prefixedSwitch = switches[typeSwitch].graphAbs().prefixed(key)
            self._graphAbs.extend(prefixedSwitch)
        for key in self._modules: 
            typeModule = self._modules[key]
            assert typeModule in modules, "Module: Invalid module: (" + key + ", " + typeModule + ")"
            if len(modules[typeModule].graphAbs().vertices()) == 0: 
                print("Module: Unconstructed module: (" + key + ", " + typeModule + ") -> Construct it. ")
                modules[typeModule].construct(units, switches, modules)
            prefixedModule = modules[typeModule].graphAbs().prefixed(key)
            self._graphAbs.extend(prefixedModule)
            prefixedFUs = modules[typeModule].fus()
            for fname, fu in prefixedFUs.items(): 
                fname = key + "." + fname
                assert not fname in self._fus, "Module: FU duplicated: " + fname
                self._fus[fname] = fu
        for splited in self._connections: 
            assert len(splited) == 2
            fr, to = splited
            assert fr in self._graphAbs.vertices(), "Module: Invalid edge source: " + fr
            assert to in self._graphAbs.vertices(), "Module: Invalid edge sink: " + to
            self._graphAbs.addEdge(fr, to, {})
    
    def info(self): 
        return "Module Name: " + self._name + "\n" + \
               " -> Module Graph: " + "\n\t".join([""] + self._graphAbs.info().split("\n"))

        #TODO: self._graph

