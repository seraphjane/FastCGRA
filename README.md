# FastCGRA: A Modeling, Mapping, and Explorartion Platform for Large-Scale CGRAs

We are still tidying the codes of FastCGRA. The codes of some algorithms are available. The binary executable of the placement algorithm is also available. 

## Experimental Settings

Intel Xeon E5-2620 v4 * 2

Ubuntu 18.04, kenerl 5.4.0

g++ 7.5.0, python 3.6.9

gurobi 9.1.2 (for the interconnection generation algorithm and CGRA-ME)

graphviz 2.40.1 (for DFG/RRG drawing, not necessary)

CGRA-ME 1.0.1 (for comparison, not necessary)

python packages: xmltodict 0.12.0, networkx 2.5, cvxpy 1.1.14, gurobi 9.1.2, graphviz 0.17

## Experiments

### CGRA and data flow modeling: 

Enter the directory: FastCGRA/description

Run optimized1.py in python3 to generate the CGRA architecture, the RRG fils is exported to the ./archs/ directory. 

Run examples.py in python3 to generate the benchmarks, the DFG fils is exported to the ./benchmarks/ directory.

### Interconnection Generation: 

Enter the directory: FastCGRA/description

Run genSwitch.py in python3 to generate a switch. 

The user can select the switch parameters by passing an arg to genSwitch.py. For example, the command 'python3 ./genSwitch.py 6x6_0.5_0' generates a 6x6 switch  with a connected ratio of 0.5. The options include: 4x4_0.5_0 4x4_0.5_1 4x4_0.5_2 4x4_0.75_0 4x4_0.75_1 4x4_0.75_2 6x6_0.5_0 6x6_0.5_1 6x6_0.5_2 6x6_0.875_0 6x6_0.875_1 6x6_0.875_2 8x8_0.5_0 8x8_0.5_1 8x8_0.5_2 8x8_0.75_0 8x8_0.75_1 8x8_0.75_2. 

The generated switch can be viewed with: python3 ./drawGraph.py ./G.txt

### Mapping on the benchmarks from CGRA-ME: 

Enter the directory: FastCGRA/placeCGRAME

export BENCH=mac

GH placer: python3 ./place_vanilla_multiprocess.py ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_DFG.txt ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_compat.txt 32

SA placer: python3 ./place_vanilla_annealing_multiprocess.py ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_DFG.txt ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_compat.txt 32

The user can also run './place_vanilla ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_DFG.txt ./benchmarks/\$\{BENCH\}/pre-gen-graph_loop_compat.txt' to view the details of the placement procedure. 

The BENCH can be selected from: mac, nomem1, simple, simple2, sum

The executables are compiled with the '-Ofast' option, which may limit their compatibility. We offer executables in the ./backup/ directory which are compiled with '-O2'. The user can try them if the default executables cannot work. 

### Mapping on the designed benchmarks: 

Enter the directory: FastCGRA/placement

export ARCH=optimized1

export BENCH=point_mul

python3 ./placeraw_multiprocess.py ./archs/\$\{ARCH\}RRG.txt ./archs/\$\{ARCH}FUs.txt ./benchmarks/\$\{ARCH\}/\$\{BENCH\}_DFG.txt ./benchmarks/\$\{ARCH\}/\$\{BENCH\}_compat.txt 32

The user can change the architecture by modifying ARCH, and use different benchmark by changing BENCH. 

The ARCH can be selected from: baseline, optimized0, optimized1. 

The BENCH can be selected from: point_add, point_mul, greater, vecmul, conv2, conv3, linear, decision_tree

The user can also run './placeraw ./archs/\$\{ARCH\}RRG.txt ./archs/\$\{ARCH\}FUs.txt ./benchmarks/\$\{ARCH\}/\$\{BENCH\}_DFG.txt ./benchmarks/\$\{ARCH\}/\$\{BENCH\}_compat.txt' to view the details of the placement procedure. 

The executable is compiled with the '-Ofast' option, which may limit its compatibility. We offer an executable in the ./backup/ directory which is compiled with '-O2'. The user can try it if the default executable cannot work. 
