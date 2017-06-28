from utils import write_csv_rows, read_csv_rows
from global_vars import *
import random
import argparse

populate_data = False
test_E_range = [1,1e12]
test_A_range = [1e-6,1e6]
test_coord_range = [0,1000] #TODO test/allow negative numbers
test_F_range = [1,1e6]

class input_table:
    def __init__(self, filename, name, headers, content=[]):
        self.filename = filename
        self.name = name
        self.headers = headers
        self.content = content

def rand_nodes(num_nodes):
    nodes = []
    for i in range(0,num_nodes):
        x = random.uniform(test_coord_range[0], test_coord_range[1])
        y = random.uniform(test_coord_range[0], test_coord_range[1])
        nodes.append([x,y])
    return nodes

def test_trusses(nodes,num_trusses):
    trusses = []
    truss_set = []
    for i in range(1,len(nodes)): #connect all nodes at least once
        E = random.uniform(test_E_range[0],test_E_range[1])
        A = random.uniform(test_A_range[0],test_A_range[1])
        trusses.append([nodes[i][0],nodes[i][1],
                        nodes[i-1][0],nodes[i-1][1],
                        E,A])
        truss_set.append([nodes[i],nodes[i-1]])
    for i in range(len(nodes),num_trusses+1): #additional random connections
        print(len(nodes))
        print(num_trusses)
        E = random.uniform(test_E_range[0],test_E_range[1])
        A = random.uniform(test_A_range[0],test_A_range[1])
        while True:
            node1 = random.randint(0,len(nodes)-1)
            node2 = random.randint(0,len(nodes)-1)
            truss_add_fwd = [[nodes[node1][0],nodes[node1][1]],
                             [nodes[node2][0],nodes[node2][1]]]
            truss_add_back = [truss_add_fwd[1],truss_add_fwd[0]]
            if (node1 != node2):
                if not (truss_add_fwd in truss_set):
                    if not (truss_add_back in truss_set):
                        break
                    else:
                        print(truss_add_back)
                        print('\nBack found in\n')
                        print(truss_set)                        
                else:
                    print(truss_add_fwd)
                    print('\nFwd found in\n')
                    print(truss_set)
        trusses.append([nodes[node1][0],nodes[node1][1],
                        nodes[node2][0],nodes[node2][1],
                        E,A])
        print('Trusses now at ' + str(len(trusses)) + ' out of ' + str(num_trusses) + '\n')
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
        Fx = random.uniform(test_F_range[0],test_F_range[1])
        Fy = random.uniform(test_F_range[0],test_F_range[1])
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

def append_test_data(tbl_content,test_data):
    for i in range(0,len(test_data)):
        tbl_content.append(test_data[i])
        return test_data

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test_data",
                    help="populate input files with test data",
                    action="store_true")
args = parser.parse_args()
    
connect_filename = 'connectivity.csv'
connect_name = 'Connectivity Table'
connect_headers = ['x1','y1','x2','y2','E','A']
connect_tbl = input_table(connect_filename,
                          connect_name,
                          connect_headers)

force_filename = 'forces.csv'
force_name = 'Force Table'
force_headers = ['x','y','Fx','Fy']
force_tbl = input_table(force_filename,
                        force_name,
                        force_headers)

bc_filename = 'boundary_conditions.csv'
bc_name = 'Boundary Conditions'
bc_headers = ['x','y','Constrained Dimension','Displacement']
bc_tbl = input_table(bc_filename,
                     bc_name,
                     bc_headers)

sim_filename = 'simulation_parameters.csv'
sim_name = 'Simulation Parameters'
sim_headers = ['Numerical Soln Multiplier','Degrees of Freedom']
sim_content = [['1e9']]
sim_tbl = input_table(sim_filename,
                      sim_name,
                      sim_headers,
                      sim_content)

def test_stdin(prompt, default):
    test_num = input(prompt + ' [' + str(default) + ']: ')
    test_num = (default if (test_num == '') else test_num)
    return int(test_num)

# Add randomly-generated test data if -t flag specified
if (args.test_data):
    num_nodes = test_stdin('Number of nodes',8)
    num_trusses = test_stdin('Number of trusses',12)
    assert (num_trusses > num_nodes)
    num_forces = test_stdin('Number of forces',3)
    assert (num_forces < num_nodes)
    num_fixed = test_stdin('Number of fixed',4)
    assert (num_fixed < num_nodes)
    
    nodes = rand_nodes(num_nodes)
    trusses = test_trusses(nodes,num_trusses)
    connect_tbl.content = append_test_data(connect_tbl.content,trusses);
    forces = test_forces(nodes,num_forces)
    force_tbl.content = append_test_data(force_tbl.content,forces)
    bcs = test_bcs(nodes,num_fixed)
    bc_tbl.content = append_test_data(bc_tbl.content,bcs)
    sim_tbl.content = [sim_tbl.content[0]+[str(num_nodes*spatial_dims)]]
    
input_files = [connect_tbl,force_tbl,bc_tbl,sim_tbl]

for i in range(0,len(input_files)):
    tbl_list = [[input_files[i].name]] +\
               [input_files[i].headers] +\
               input_files[i].content
    write_csv_rows(input_files[i].filename,tbl_list)
    print(input_files[i].name + ' written to ' +\
          input_files[i].filename)
