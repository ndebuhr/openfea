from utils import write_csv_rows, read_csv_rows
from classes import truss, force, fixed_node
from global_vars import *
import numpy as np #for development debug/format only

class parse_var:
    def __init__(self, descript_name, val=None, class_name=None):
        self.descript_name = descript_name

class output_table:
    def __init__(self, filename, content=None):
        self.filename = filename
        
def blanks_exist(tbl):
    for i in range(2,len(tbl)): #Don't check first (table name) row
        if (len(tbl[i]) != len(tbl[i-1])):
            return True
        for j in range(0,len(tbl[i])):
            if (tbl[i][j] == ''):
                return True
    return False

def define_nodes(tbl_content):
    assert not blanks_exist(tbl_content),\
        'Connectivity table values must not be left blank'
    ind_x1 = tbl_content[1].index('x1')
    ind_y1 = tbl_content[1].index('y1')
    ind_x2 = tbl_content[1].index('x2')
    ind_y2 = tbl_content[1].index('y2')
    coord_pairs = []
    for i in range(2,len(tbl_content)):
        coord_pairs.append([tbl_content[i][ind_x1],
                            tbl_content[i][ind_y1]])
        coord_pairs.append([tbl_content[i][ind_x2],
                            tbl_content[i][ind_y2]])
    for i in range(0,len(coord_pairs)):
        coord_pairs[i] = '-'.join(coord_pairs[i])
    coord_pairs = set(coord_pairs) #remove non-uniques
    coord_pairs = list(coord_pairs)
    for i in range(0,len(coord_pairs)):
        coord_pairs[i] = coord_pairs[i].split('-')
    for i in range(0,len(coord_pairs)):
        coord_pairs[i][0] = float(coord_pairs[i][0])
        coord_pairs[i][1] = float(coord_pairs[i][1])
    coord_pairs.sort()
    for i in range(0,len(coord_pairs)):
        coord_pairs[i].append(i)
    return coord_pairs
        
def read_connectivity(tbl_content, node_coords):
    assert not blanks_exist(tbl_content),\
        'Connectivity table values must not be left blank'
    ind_x1 = tbl_content[1].index('x1')
    ind_y1 = tbl_content[1].index('y1')
    ind_x2 = tbl_content[1].index('x2')
    ind_y2 = tbl_content[1].index('y2')
    ind_E = tbl_content[1].index('E')
    ind_A = tbl_content[1].index('A')
    trusses = []
    for i in range(2,len(tbl_content)): #content rows only
        x1 = float(tbl_content[i][ind_x1])
        y1 = float(tbl_content[i][ind_y1])
        x2 = float(tbl_content[i][ind_x2])
        y2 = float(tbl_content[i][ind_y2])
        node1 = node_coords.index([x1,y1])
        node2 = node_coords.index([x2,y2])
        E = float(tbl_content[i][ind_E])
        assert (E>0)
        A = float(tbl_content[i][ind_A])
        assert (A>0)
        trusses.append(truss(x1,x2,y1,y2,E,A,node1,node2))
    print('Read ' + str(len(trusses)) + ' trusses' +\
          ' from connectivity table')
    return trusses

def read_forces(tbl_content, node_coords):
    assert not blanks_exist(tbl_content),\
        'Forces table values must not be left blank'
    ind_x = tbl_content[1].index('x')
    ind_y = tbl_content[1].index('y')
    ind_fx = tbl_content[1].index('Fx')
    ind_fy = tbl_content[1].index('Fy')
    forces = []
    for i in range(2,len(tbl_content)):
        x = float(tbl_content[i][ind_x])
        y = float(tbl_content[i][ind_y])
        fx = float(tbl_content[i][ind_fx])
        fy = float(tbl_content[i][ind_fy])
        node = node_coords.index([x,y])
        forces.append(force(fx,fy,node))
    print('Read ' + str(len(forces)) + ' forces' +\
          ' from forces table')
    return forces

def read_bcs(tbl_content, node_coords):
    assert not blanks_exist(tbl_content),\
        'Boundary conditions table values must not be left blank'
    ind_x = tbl_content[1].index('x')
    ind_y = tbl_content[1].index('y')
    ind_xory = tbl_content[1].index('Constrained Dimension')
    ind_disp = tbl_content[1].index('Displacement')
    bcs = []
    for i in range(2,len(tbl_content)):
        x = float(tbl_content[i][ind_x])
        y = float(tbl_content[i][ind_y])
        x_or_y = tbl_content[i][ind_xory]
        assert ( (x_or_y=='x') | (x_or_y=='y') )
        disp = float(tbl_content[i][ind_disp])
        node = node_coords.index([x,y])
        bcs.append(fixed_node(node,x_or_y,disp))
    print('Read ' + str(len(bcs)) + ' boundary conditions' +\
          ' from boundary conditions table')
    return bcs
        
def read_params(tbl_content, var_list):
    assert not blanks_exist(tbl_content),\
        'Simulation parameters table values must not be left blank'
    for i in range(0,len(tbl_content)):
        for j in range(0,len(tbl_content[i])):
            for k in range(0,len(var_list)):
                if (tbl_content[i][j]==var_list[k].descript_name):
                    var_list[k].val=tbl_content[i+1][j]
                    print('Set ' + var_list[k].descript_name +\
                            ' to ' + str(var_list[k].val))
    return var_list

def get_data():

    connect_tbl=output_table('connectivity.csv')
    force_tbl=output_table('forces.csv')
    bc_tbl=output_table('boundary_conditions.csv')
    sim_tbl=output_table('simulation_parameters.csv')
    
    output_files=[connect_tbl,force_tbl,bc_tbl,sim_tbl]

    # Read in content and convert to nested list
    for i in range(0,len(output_files)):
        output_files[i].content = read_csv_rows(output_files[i].filename)
        for j in range(0,len(output_files[i].content)):
            output_files[i].content[j]=output_files[i].content[j].split(',')
        print('Successfully read ' + output_files[i].filename)
            
            # for i in range(0,len(output_files)):
            #     print(output_files[i].filename)
            #     print(output_files[i].content)
            
    num_mult = parse_var(descript_name='Numerical Soln Multiplier')
    dof = parse_var(descript_name='Degrees of Freedom')
    sim_params = [num_mult,dof]
        
    print('\n')
    sim_params = read_params(sim_tbl.content,sim_params)
    sim_params[0].val = float(sim_params[0].val)
    sim_params[1].val = int(sim_params[1].val)
    assert (sim_params[0].val > 0)
    assert (sim_params[1].val % spatial_dims == 0)
    assert (sim_params[1].val > 0)
    
    # for i in range(0,len(sim_params)):
    #     print(sim_params[i].descript_name)
    #     print(sim_params[i].val)
    
    nodes = define_nodes(connect_tbl.content)
    node_coords = []
    for i in range(0,len(nodes)):
        node_coords.append(nodes[i][0:2])
        
    trusses = read_connectivity(connect_tbl.content,node_coords)
        # for i in range(0,len(trusses)):
        #     print(trusses[i].x1,trusses[i].x2,trusses[i].node1,trusses[i].node2)

    forces = read_forces(force_tbl.content,node_coords)
    # for i in range(0,len(forces)):
    #     print(forces[i].fx, forces[i].fy, forces[i].node)

    fixed_nodes = read_bcs(bc_tbl.content,node_coords)
    # for i in range(0,len(fixed_nodes)):
    #     print(fixed_nodes[i].node, fixed_nodes[i].x_or_y,
    #           fixed_nodes[i].disp)

    return trusses, forces, fixed_nodes, sim_params
