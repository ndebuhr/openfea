import numpy as np
import matplotlib.pyplot as plt
import truss_struct as ts

def get_max_stress(trusses):
    max_stress = trusses[0].stress
    for i in range(0,len(trusses)):
        if (abs(trusses[i].stress) > max_stress):
            max_stress = abs(trusses[i].stress)
    return max_stress

def get_line_color(stress, max_stress):
    # Color range from black (no stress) to red (max stress)
    perc_of_max = abs(stress)/abs(max_stress)
    return [perc_of_max,0,0]

u, stresses, R, trusses = ts.calc_solution()

max_stress = get_max_stress(trusses)
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
    # Provide annotative text next to truss, with stress quantity
    plt.text((x1+x2)/2, (y1+y2)/2, r'$\sigma='+('%.4E' % stress )+'$')

plt.title('Truss Stresses')
plt.gca().set_aspect('equal', adjustable='box') # No geometric skew
plt.show()
