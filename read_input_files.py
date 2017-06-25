from utils import write_csv_rows, read_csv_rows
from classes import truss, force, fixed_node

class parse_var:
    def __init__(self, descript_name, val=None, class_name):
        self.descript_name = descript_name

class output_table:
    def __init__(self, filename, content=None):
        self.filename = filename

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

for i in range(0,len(output_files)):
    print(output_files[i].filename)
    print(output_files[i].content)

c = parse_var(descript_name='Numerical Soln Multiplier')
dof = parse_var(descript_name='Degrees of Freedom')
