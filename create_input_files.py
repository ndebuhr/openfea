from utils import write_csv_rows, read_csv_rows
from global_vars import *
import random
import argparse

populate_data = False
test_E_range = {'min': 1,
                'max': 1e12}
test_A_range = {'min': 1e-6,
                'max': 1e6}
test_coord_range = {'min': 0,
                    'max': 1000} #TODO test/allow negative numbers
test_F_range = {'min': 1,
                'max': 1e6}

class input_table:
    def __init__(self, filename, name, headers, content=[]):
        self.filename = filename
        self.name = name
        self.headers = headers
        self.content = content

def rand_nodes(num_nodes):
    nodes = []
    for i in range(0,num_nodes):
        x = random.uniform(test_coord_range['min'], test_coord_range['max'])
        y = random.uniform(test_coord_range['min'], test_coord_range['max'])
        nodes.append([x,y])
    return nodes

def bridge_nodes(nodes, num_base):
    for i in range(0,num_base):
        x = 1000*i/(num_base-1)
        y = 0
        nodes.append([x,y])
    nodes.append(nodes.pop(0))
    return nodes

def test_trusses(nodes,num_trusses):
    def truss_already_exists(nodes,node1,node2,truss_set):
        # Checks A->B against existing A->B and B->A
        truss_add_fwd = [[nodes[node1][0],nodes[node1][1]], #x1,y1
                         [nodes[node2][0],nodes[node2][1]]] #x2,y2
        truss_add_back = [truss_add_fwd[1], #x2,y2
                          truss_add_fwd[0]] #x1,y1
        if (truss_add_fwd in truss_set):
            return True
        if (truss_add_back in truss_set):
            return True
        return False
    trusses = []
    truss_set = []
    for i in range(1,len(nodes)): #connect all nodes at least once
        truss = {}
        truss['E'] = random.uniform(test_E_range['min'],test_E_range['max'])
        truss['A'] = random.uniform(test_A_range['min'],test_A_range['max'])
        truss['x1'] = nodes[i][0]
        truss['y1'] = nodes[i][1]
        truss['x2'] = nodes[i-1][0]
        truss['y2'] = nodes[i-1][1]
        trusses.append([truss['x1'],truss['y1'],truss['x2'],truss['y2'],
                        truss['E'],truss['A']])
        truss_set.append([nodes[i],nodes[i-1]])
    for i in range(len(nodes),num_trusses+1): #additional random connections
        truss = {}
        truss['E'] = random.uniform(test_E_range['min'],test_E_range['max'])
        truss['A'] = random.uniform(test_A_range['min'],test_A_range['max'])
        while True:
            node1 = random.randint(0,len(nodes)-1)
            node2 = random.randint(0,len(nodes)-1)
            if (node1 != node2):
                if not truss_already_exists(nodes,node1,node2,truss_set):
                    break
        truss['x1'] = nodes[node1][0]
        truss['y1'] = nodes[node1][1]
        truss['x2'] = nodes[node2][0]
        truss['y2'] = nodes[node2][1]
        truss_set.append([[truss['x1'],
                           truss['y1']],
                          [truss['x2'],
                           truss['y2']]])
        trusses.append([truss['x1'],
                        truss['y1'],
                        truss['x2'],
                        truss['y2'],
                        truss['E'],
                        truss['A']])
    return trusses

def split_trusses(nodes, trusses):
    def get_intersection(m,b):
        x = (b[1]-b[0])/(m[0]-m[1])
        y = m[0]*x+b[0]
        return x, y
    def check_intersection(x,y,nodes1,nodes2,shared_node):
        if shared_node:
            return False
        checks = [[False,False], #for truss 1
                  [False,False]] #for truss 2
        nodes = [nodes1,nodes2]
        for i in range(0,2):
            node_bounds = nodes[i]
            x1 = node_bounds[0][0]
            x2 = node_bounds[1][0]
            y1 = node_bounds[0][1]
            y2 = node_bounds[1][1]
            if (x1 < x) and (x < x2):
                checks[i][0] = True
            if (x2 < x) and (x < x1):
                checks[i][0] = True
            if (y1 < y) and (y < y2):
                checks[i][1] = True
            if (y2 < y) and (y < y1):
                checks[i][1] = True
        for i in range(0,len(checks)):
            if False in checks[i]:
                return False
        return True
    def unique_nodes(nodes):
        checked = []
        for e in nodes:
            if e not in checked:
                checked.append(e)
        return checked
    for i in range(0,len(trusses)):
        n1 = [trusses[i][0], trusses[i][1]]
        n2 = [trusses[i][2], trusses[i][3]]
        nodes1 = [n1,n2]
        E1 = trusses[i][4]
        A1 = trusses[i][5]
        for j in range(0,len(trusses)):
            if (i != j):
                n1 = [trusses[j][0], #x1
                      trusses[j][1]] #y1
                n2 = [trusses[j][2], #x2
                      trusses[j][3]] #y2
                nodes2 = [n1,n2]
                E2 = trusses[j][4]
                A2 = trusses[j][5]
                m = [(trusses[i][3]-trusses[i][1])/(trusses[i][2]-trusses[i][0])]
                b = [trusses[i][1]-m[0]*trusses[i][0]]
                m.append((trusses[j][3]-trusses[j][1])/(trusses[j][2]-trusses[j][0]))
                b.append(trusses[j][1]-m[1]*trusses[j][0])
                if (m[0] != m[1]): # if trusses are not parallel
                    x, y = get_intersection(m,b)
                    all_nodes = nodes1+nodes2
                    set_nodes = unique_nodes(all_nodes)
                    if (len(all_nodes) != len(set_nodes)):
                        shared_node = True #if trusses share a node
                    else:
                        shared_node = False
                    if (check_intersection(x,y,nodes1,nodes2,shared_node)):
                        trusses.append([nodes1[0][0],nodes1[0][1],x,y,E1,A1])
                        trusses.append([x,y,nodes1[1][0],nodes1[1][1],E1,A1])
                        trusses.append([nodes2[0][0],nodes2[0][1],x,y,E2,A2])
                        trusses.append([x,y,nodes2[1][0],nodes2[1][1],E2,A2])
                        if ( i < j ):
                            trusses.pop(j)
                            trusses.pop(i)
                        else:
                            trusses.pop(i)
                            trusses.pop(j)
                        nodes.append([x,y])
                        i=0 #Restart truss intersection checking
                        j=0
    return nodes, trusses
                        
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
        Fx = random.uniform(test_F_range['min'],test_F_range['max'])
        Fy = random.uniform(test_F_range['min'],test_F_range['max'])
        if (random.randint(0,1)):
            if (random.randint(0,1)): #choose x or y by random
                Fx = 0
            else:
                Fy = 0
        forces.append([x,y,Fx,Fy])
    return forces

def bridge_forces(num_base):
    forces = []
    for i in range(1,num_base-1):
        forces.append([1000*i/(num_base-1),0,0,-10000])
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
        if (random.randint(0,1)==1): #choose x or y randomly
            x_or_y = 'x'
        else:
            x_or_y = 'y'
        bcs.append([nodes[node][0],nodes[node][1],
                    x_or_y,0])
    return bcs

def bridge_bcs():
    bcs = []
    # x,y,direction,disp
    bcs.append([0,0,'x',0])
    bcs.append([0,0,'y',0])
    bcs.append([1000,0,'x',0])
    bcs.append([1000,0,'y',0])
    return bcs

def append_test_data(tbl_content,test_data):
    for i in range(0,len(test_data)):
        tbl_content.append(test_data[i])
        return test_data

def test_stdin(prompt, default):
    test_num = input(prompt + ' [' + str(default) + ']: ')
    test_num = (default if (test_num == '') else test_num)
    return int(test_num)

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test_data",
                    help="populate input files with test data",
                    action="store_true")
parser.add_argument("-b", "--bridge",
                    help="create random bridge designs",
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

def prune_truss(nodes,trusses):
    new_truss_set = []
    top_truss = trusses[:]
    for i in range(0,len(top_truss)):
        pop_truss = trusses.pop(i)
        remove_node_1 = True
        remove_node_2 = True
        for j in range(0,len(trusses)):
            if (pop_truss[0] in trusses[j]) and (pop_truss[1] in trusses[j]):
                remove_node_1 = False
            if (pop_truss[2] in trusses[j]) and (pop_truss[3] in trusses[j]):
                remove_node_2 = False
        if (remove_node_1):
            nodes.pop(nodes.index([pop_truss[0],pop_truss[1]]))
            print('Removed One!')
        if (remove_node_2):
            nodes.pop(nodes.index([pop_truss[2],pop_truss[3]]))
            print('Removed One!')
        if (remove_node_1 == False) and (remove_node_2 == False):
            new_truss_set.append(pop_truss)
        trusses = trusses[0:i] + [pop_truss] + trusses[i:]
    return nodes, new_truss_set
        
if (args.bridge):
    num_nodes = 8
    num_trusses = 12
    num_forces = 3
    nodes = rand_nodes(num_nodes)
    num_base = 2
    nodes = bridge_nodes(nodes, num_base)
    trusses = test_trusses(nodes,num_trusses)
    nodes, trusses = split_trusses(nodes,trusses)
    # TODO Remove workaround below and actually solve issue
    nodes, trusses = split_trusses(nodes,trusses)
    nodes, trusses = prune_truss(nodes, trusses)
    forces = test_forces(nodes,num_forces)
    bcs = bridge_bcs()
    connect_tbl.content = append_test_data(connect_tbl.content,trusses);
    force_tbl.content = append_test_data(force_tbl.content,forces)
    bc_tbl.content = append_test_data(bc_tbl.content,bcs)
    sim_tbl.content = [sim_tbl.content[0]+\
                      [str(len(nodes)*spatial_dims)]]
    
# Add randomly-generated test data if -t flag specified
if (args.test_data):
    num_nodes = test_stdin('Number of nodes',5)
    num_trusses = test_stdin('Number of trusses',8)
    assert (num_trusses > num_nodes)
    num_forces = test_stdin('Number of forces',2)
    assert (num_forces < num_nodes)
    num_fixed = test_stdin('Number of fixed',3)
    assert (num_fixed < num_nodes)
    
    nodes = rand_nodes(num_nodes)
    trusses = test_trusses(nodes,num_trusses)
    nodes, trusses = split_trusses(nodes,trusses)
    connect_tbl.content = append_test_data(connect_tbl.content,trusses);
    forces = test_forces(nodes,num_forces)
    force_tbl.content = append_test_data(force_tbl.content,forces)
    bcs = test_bcs(nodes,num_fixed)
    bc_tbl.content = append_test_data(bc_tbl.content,bcs)
    sim_tbl.content = [sim_tbl.content[0]+[str(len(nodes)*spatial_dims)]]
    
input_files = [connect_tbl,force_tbl,bc_tbl,sim_tbl]

for i in range(0,len(input_files)):
    tbl_list = [[input_files[i].name]] +\
               [input_files[i].headers] +\
               input_files[i].content
    write_csv_rows(input_files[i].filename,tbl_list)
    print(input_files[i].name + ' written to ' +\
          input_files[i].filename)
