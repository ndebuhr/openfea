import numpy as np
import read_input_files as rif
from scipy.optimize import fsolve
from scipy.optimize import minimize
from classes import truss, force, fixed_node

trusses, forces, fixed_nodes, sim_params = rif.get_data()

numerical_mult = sim_params[0].val
spatial_dims = 2

def compile_K(dof, trusses):
    K = np.zeros((dof, dof))
    for i in range(0,len(trusses)):
        for j in range(0,2):
            for k in range(0,2):
                node1 = trusses[i].node1
                node2 = trusses[i].node2
                K[j+spatial_dims*node1][k+spatial_dims*node1] += trusses[i].K2D[j][k]
                K[j+spatial_dims*node1][k+spatial_dims*node2] += trusses[i].K2D[j][k+2]
                K[j+spatial_dims*node2][k+spatial_dims*node1] += trusses[i].K2D[j+2][k]
                K[j+spatial_dims*node2][k+spatial_dims*node2] += trusses[i].K2D[j+2][k+2]
    return K

def compile_F(dof, forces):
    F = np.zeros((dof,1))
    for i in range(0,len(forces)):
        node = forces[i].node
        F[node*spatial_dims][0] += forces[i].fx
        F[node*spatial_dims+1][0] += forces[i].fy
    return F

def fix_nodes(K, F, c, fixed_nodes):
    for i in range(0,len(fixed_nodes)):
        if (fixed_nodes[i].x_or_y == 'x'):
            ind = spatial_dims*fixed_nodes[i].node
        if (fixed_nodes[i].x_or_y == 'y'):
            ind = spatial_dims*fixed_nodes[i].node+1
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
        node1 = truss.node1
        node2 = truss.node2
        u_local[0][0] = u[truss.node1*spatial_dims][0]
        u_local[1][0] = u[truss.node1*spatial_dims+1][0]
        u_local[2][0] = u[truss.node2*spatial_dims][0]
        u_local[3][0] = u[truss.node2*spatial_dims+1][0]
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

    return u, stresses, R, trusses
