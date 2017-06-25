import numpy as np

class truss:
    def __init__(self, x1, x2, y1, y2, E, A,
                 node1, node2, stress=None, strain=None):
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
