from utils import write_csv_rows, read_csv_rows
import random

num_nodes = 8
num_trusses = 12
num_forces = 3
num_fixed = 4

class input_table:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

def rand_nodes(num_nodes):
    nodes = []
    for i in range(0,num_nodes):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        nodes.append([x,y])
    return nodes

def test_trusses(nodes,num_trusses):
    trusses = []
    for i in range(1,len(nodes)): #connect all nodes at least once
        E = random.uniform(1,1e12)
        A = random.uniform(1e-6,1e6)
        trusses.append([nodes[i][0],nodes[i][1],
                        nodes[i-1][0],nodes[i-1][1],
                        E,A])
    for i in range(num_trusses-len(nodes)-1): #additional random connections
        E = random.uniform(1,1e12)
        A = random.uniform(1e-6,1e6)
        while True:
            node1 = random.randint(0,len(nodes)-1)
            node2 = random.randint(0,len(nodes)-1)
            if (node1 != node2):
                break
        trusses.append([nodes[node1][0],nodes[node1][1],
                        nodes[node2][0],nodes[node2][1],
                        E,A])
    return trusses        

def test_forces(nodes, num_forces):
    forces = []
    force_nodes = []
    while True:
        new_node = random.randint(0,len(nodes)-1)
        force_nodes.append(new_node)
        force_nodes = set(force_nodes)
        force_nodes = list(force_nodes)
        if len(force_nodes)==num_forces:
            break
    for i in range(0,num_forces):
        node = force_nodes[i]
        x = nodes[node][0]
        y = nodes[node][1]
        Fx = random.uniform(1,1e6)
        Fy = random.uniform(1,1e6)
        forces.append([x,y,Fx,Fy])
    return forces

def test_bcs(nodes, num_fixed):
    bcs = []
    fix_nodes = []
    while True:
        new_node = random.randint(0,len(nodes)-1)
        fix_nodes.append(new_node)
        fix_nodes = set(fix_nodes)
        fix_nodes = list(fix_nodes)
        if len(fix_nodes)==num_fixed:
            break
    for i in range(0,num_fixed):
        node = fix_nodes[i]
        if (random.randint(0,1)==1):
            x_or_y = 'x'
        else:
            x_or_y = 'y'
        bcs.append([nodes[node][0],nodes[node][1],
                    x_or_y,0])
    return bcs
    
nodes = rand_nodes(num_nodes)

connect_list = [['Connectivity Table'],
                ['x1','y1','x2','y2','E','A']]
trusses = test_trusses(nodes,num_trusses)
for i in range(0,len(trusses)):
    connect_list.append(trusses[i])
connect_tbl = input_table('connectivity.csv',
                          connect_list)

force_list = [['Force Table'],
              ['x','y','Fx','Fy']]
forces = test_forces(nodes,num_forces)
for i in range(0,len(forces)):
    force_list.append(forces[i])
force_tbl = input_table('forces.csv',
                        force_list)

bc_list = [['Boundary Conditions'],
           ['x','y','Constrained Dimension','Displacement']]
bcs = test_bcs(nodes,num_fixed)
for i in range(0,len(bcs)):
    bc_list.append(bcs[i])
bc_tbl = input_table('boundary_conditions.csv',
                     bc_list)

sim_tbl = input_table('simulation_parameters.csv',
                      [['Simulation Parameters'],
                       ['Numerical Soln Multiplier','Degrees of Freedom'],
                       ['1e9',str(num_nodes*2)]])

input_files = [connect_tbl,force_tbl,bc_tbl,sim_tbl]

for i in range(0,len(input_files)):
    write_csv_rows(input_files[i].filename,input_files[i].content)
    print(input_files[i].content[0][0] + ' written to ' + input_files[i].filename)
