import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import minimize

numerical_mult = 1e9

class truss:
    def __init__(self, x1, x2, y1, y2, E, A,
                 node1, node2, stress=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.E = E
        self.A = A
        self.l = ((x2-x1)**2+(y2-y1)**2)**(1/2)
        self.cos_t = (x2-x1)/self.l
        self.sin_t = (y2-y1)/self.l
        self.L = [[self.cos_t, self.sin_t, 0, 0],
                  [0, 0, self.cos_t, self.sin_t]]
        self.eL = [-self.cos_t, -self.sin_t, self.cos_t, self.sin_t]
        # K1D definition assumes a linear approximation
        # for the truss displacement function
        self.K1D = [[self.E*self.A/self.l, -self.E*self.A/self.l],
                    [-self.E*self.A/self.l, self.E*self.A/self.l]]
        self.K2D = (np.matrix(self.L).getT()*np.matrix(self.K1D)*\
                   np.matrix(self.L)).tolist()
        self.node1 = node1 #zero-indexed
        self.node2 = node2 #zero-indexed

class force:
    def __init__(self, fx, fy, node):
        self.fx = fx
        self.fy = fy
        self.node = node

class fixed_node:
    def __init__(self, node, x_or_y, disp):
        self.node = node
        self.x_or_y = x_or_y
        self.disp = disp
        
def compile_K(dof, trusses):
    K = np.zeros((dof, dof))
    for i in range(0,len(trusses)):
        for j in range(0,2):
            for k in range(0,2):
                node1 = trusses[i].node1
                node2 = trusses[i].node2
                K[j+2*node1][k+2*node1] += trusses[i].K2D[j][k]
                K[j+2*node1][k+2*node2] += trusses[i].K2D[j][k+2]
                K[j+2*node2][k+2*node1] += trusses[i].K2D[j+2][k]
                K[j+2*node2][k+2*node2] += trusses[i].K2D[j+2][k+2]
    return K

def compile_F(dof, forces):
    F = np.zeros((dof,1))
    for i in range(0,len(forces)):
        node = forces[i].node
        F[node][0] += forces[i].fx
        F[node+1][0] += forces[i].fy
    return F

def fix_nodes(K, F, c, fixed_nodes):
    for i in range(0,len(fixed_nodes)):
        if (fixed_nodes[i].x_or_y == 'x'):
            ind = 2*fixed_nodes[i].node
        if (fixed_nodes[i].x_or_y == 'y'):
            ind = 2*fixed_nodes[i].node+1
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
        if (K[i][i]>K_max):
            K_max = K[i][i] #check diagonals only
    return mult*K_max

def assign_stresses(u, trusses):
    for i in range(0,len(trusses)):
        truss = trusses[i]
        disp1 = u[truss.node1][0]
        disp2 = u[truss.node2][0]
        truss.stress = (truss.E/truss.l)*(disp2-disp1)

dof = int(input('Number of nodes: '))*2

A = truss(x1=0.5,x2=0,y1=0.3,y2=0.3,
          E=70e9,A=200*1e-6,node1=0,node2=1)
B = truss(x1=0.5,x2=0.9,y1=0.3,y2=0,
          E=70e9,A=200*1e-6,node1=0,node2=2)
trusses = [A,B]

f1 = force(fx=0,fy=-12e3,node=0)
forces = [f1]

n1 = fixed_node(1,'x',0)
n2 = fixed_node(1,'y',0)
n3 = fixed_node(2,'x',0)
n4 = fixed_node(2,'y',0)
fixed_nodes=[n1,n2,n3,n4]

K = compile_K(dof,trusses)
F = compile_F(dof,forces)

c = set_c(K,numerical_mult)
K, F = fix_nodes(K,F,c,fixed_nodes)
u = solve_u(K,F)
assign_stresses(u,trusses)

for i in range(0, len(trusses)):
    print(trusses[i].stress)

print(K,len(K))
print(F,len(F))
print(u,len(u))
