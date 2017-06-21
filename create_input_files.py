from utils import write_csv_rows, read_csv_rows

class input_table:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

connect_tbl=input_table('connectivity.csv',
                        [['Connectivity Table'],
                         ['x1','y1','x2','y2','E','A']])
force_tbl=input_table('forces.csv',
                      [['Force Table'],
                       ['x','y','Fx','Fy']])
bc_tbl=input_table('boundary_conditions.csv',
                   [['Boundary Conditions'],
                    ['x','y','Constrained Dimension','Displacement']])
sim_tbl=input_table('simulation_parameters.csv',
                    [['Simulation Parameters'],
                     ['Numerical Soln Multiplier','Degrees of Freedom'],
                     ['1e9']])

input_files=[connect_tbl,force_tbl,bc_tbl,sim_tbl]

for i in range(0,len(input_files)):
    write_csv_rows(input_files[i].filename,input_files[i].content)
    print(input_files[i].content[0][0] + ' written to ' + input_files[i].filename)
