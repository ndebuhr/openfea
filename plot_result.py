import numpy as np
import matplotlib.pyplot as plt
import truss_struct as ts

def get_max_stress(trusses):
    max_stress = trusses[0].stress
    for i in range(0,len(trusses)):
        if (abs(trusses[i].stress) > max_stress):
            max_stress = abs(trusses[i].stress)
    return max_stress

def get_max_dim(trusses):
    max_dim = trusses[0].x1
    for i in range(0,len(trusses)):
        truss_max = max(abs(trusses[i].x1), abs(trusses[i].x2),
                        abs(trusses[i].y1), abs(trusses[i].y2))
        if (truss_max > max_dim):
            max_dim = truss_max
    return truss_max

def get_line_color(stress, max_stress):
    # Color range from black (no stress) to red (max stress)
    perc_of_max = abs(stress)/abs(max_stress)
    return [perc_of_max,0,0]

def node_lookup(trusses):
    nodes_set = {}
    for i in range(0,len(trusses)):
        nodes_set[str(trusses[i].node1)] = [trusses[i].x1,trusses[i].y1]
        nodes_set[str(trusses[i].node2)] = [trusses[i].x2,trusses[i].y2]
    return nodes_set

forces, u, stresses, R, trusses, fixed_nodes = ts.calc_solution()

max_stress = get_max_stress(trusses)
max_dim = get_max_dim(trusses)
nodes_set = node_lookup(trusses)

plt.figure(1)

for i in range(0,len(trusses)):
    x1 = trusses[i].x1
    x2 = trusses[i].x2
    y1 = trusses[i].y1
    y2 = trusses[i].y2
    stress = trusses[i].stress
    line_color = get_line_color(stress,max_stress)
    # Plot the truss on the figure
    plt.plot([x1, x2], [y1, y2], color=line_color)
    plt.scatter(x1, y1, 25, c="g", alpha=0.9)
    plt.scatter(x2, y2, 25, c="g", alpha=0.9)
    # Provide annotative text next to truss, with stress quantity
    plt.text((x1+x2)/2, (y1+y2)/2, r'$\sigma='+('%.4E' % stress )+'$')

for i in range(0,len(forces)):
    if (forces[i].fx != 0):
        xy = nodes_set[str(forces[i].node)]
        x = xy[0]
        y = xy[1]
        plt.arrow(x, y, max_dim/30, 0, fc="b", ec="b", head_width=max_dim/80, head_length=max_dim/40 )
    if (forces[i].fy != 0):
        xy = nodes_set[str(forces[i].node)]
        x = xy[0]
        y = xy[1]
        plt.arrow(x, y, 0, max_dim/30, fc="b", ec="b", head_width=max_dim/80, head_length=max_dim/40 )

for i in range(0,len(fixed_nodes)):
    xy = nodes_set[str(fixed_nodes[i].node)]
    x = xy[0]
    y = xy[1]
    x_delta = max_dim
    if (fixed_nodes[i].x_or_y=='x'):
        plt.plot([x,x],[y-max_dim/40,y+max_dim/40],
                 color=[1,0,1],linewidth=2)
    if (fixed_nodes[i].x_or_y=='y'):
        plt.plot([x-max_dim/40, x+max_dim/40],[y,y],
                 color=[1,0,1],linewidth=2)

plt.title('Truss Stresses')
plt.gca().set_aspect('equal', adjustable='box') # No geometric skew

xmin, xmax = plt.xlim()
lim_width = xmax-xmin
xmin = xmin-0.1*lim_width
xmax = xmax+0.1*lim_width
plt.xlim( xmin, xmax )

ymin, ymax = plt.ylim()
lim_height = xmax-xmin
ymin = ymin-0.1*lim_height
ymax = ymax+0.1*lim_height
plt.ylim( ymin, ymax )

plt.show()
