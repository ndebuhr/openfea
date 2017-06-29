from scipy.optimize import fsolve
from scipy.optimize import minimize
from classes import truss, force, fixed_node
from global_vars import *
import numpy as np
import read_input_files as rif

trusses, forces, fixed_nodes, sim_params = rif.get_data()

numerical_mult = sim_params[0].val

def compile_K(dof, trusses):
    K = np.zeros((dof, dof))
    for i in range(0,len(trusses)):
        for j in range(0,spatial_dims):
            for k in range(0,spatial_dims):
                nodes = [trusses[i].node1, trusses[i].node2]
                K[j+spatial_dims*nodes[0]][k+spatial_dims*nodes[0]] += trusses[i].K2D[j][k]
                K[j+spatial_dims*nodes[0]][k+spatial_dims*nodes[1]] += trusses[i].K2D[j][k+spatial_dims]
                K[j+spatial_dims*nodes[1]][k+spatial_dims*nodes[0]] += trusses[i].K2D[j+spatial_dims][k]
                K[j+spatial_dims*nodes[1]][k+spatial_dims*nodes[1]] += trusses[i].K2D[j+spatial_dims][k+spatial_dims]
    return K

def compile_F(dof, forces):
    F = np.zeros((dof,1))
    for i in range(0,len(forces)):
        node = forces[i].node
        force_dims = [forces[i].fx, forces[i].fy]
        for i in range(0,spatial_dims):
            F[node*spatial_dims+i][0] += force_dims[i]
    return F

def fix_nodes(K, F, c, fixed_nodes):
    dim_set = ['x','y'] #TODO improve dimension extensibility
    for i in range(0,len(fixed_nodes)):
        for j in range(0,spatial_dims):
            if (fixed_nodes[i].x_or_y == dim_set[j]):
                ind = spatial_dims*fixed_nodes[i].node+j
        K[ind][ind] += c
        F[ind][0] += c*fixed_nodes[i].disp
    return K, F

def solve_u(K, F):
    u_matrix = np.matrix(K).getI()*np.matrix(F)
    u_list = u_matrix.tolist()
    return u_list

def set_c(K,mult):
    K_max = K[0][0]
    for i in range(0,len(K)):
        if (K[i][i] > K_max):
            K_max = K[i][i] #check diagonals only
    return mult*K_max

def assign_stresses(u, trusses):
    for i in range(0,len(trusses)):
        u_local = np.zeros((4,1))
        truss = trusses[i]
        nodes = [truss.node1, truss.node2]
        for j in range(0,spatial_dims):
            u_local[j][0] = u[nodes[0]*spatial_dims+j][0]
            u_local[spatial_dims+j][0] = u[nodes[1]*spatial_dims+j][0]
        stress = (truss.E/truss.l)*np.matrix(truss.eL)*\
                 np.matrix(u_local)
        truss.stress = stress.tolist()[0][0]
        truss.strain = truss.stress/truss.E

def calc_solution():        
    dof = sim_params[1].val
    
    K = compile_K(dof,trusses)
    F = compile_F(dof,forces)
    
    c = set_c(K,numerical_mult)
    K, F = fix_nodes(K,F,c,fixed_nodes)
    u = solve_u(K,F)
    assign_stresses(u,trusses)
    
    K_orig = compile_K(dof,trusses)
    F_orig = compile_F(dof,forces)
    R = np.matrix(K_orig)*np.matrix(u)-np.matrix(F_orig)
    R = R.tolist()
    
    stresses = []
    for i in range(0, len(trusses)):
        stresses.append(trusses[i].stress)
        
    print('\nDisplacements\n',np.matrix(u))
    print('\nStresses\n',np.matrix(stresses))
    print('\nReactions\n',np.matrix(R))

    return forces, u, stresses, R, trusses
