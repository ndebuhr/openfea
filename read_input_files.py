from utils import write_csv_rows, read_csv_rows
from classes import truss, force, fixed_node

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
    if blanks_exist(tbl_content):
        print('Table values must not be left blank')
        return 1 #Stop function execution
    ind_x1 = tbl_content[1].index('x1')
    ind_y1 = tbl_content[1].index('y1')
    ind_x2 = tbl_content[1].index('x2')
    ind_y2 = tbl_content[1].index('y2')
    coord_pairs = []
    for i in range(2,len(tbl_content)):
        coord_pairs.append([ind_x1,ind_y1])
        coord_pairs.append([ind_x2,ind_y2])
    coord_pairs = Set(coord_pairs) #remove uniques
    coord_pairs = list(coord_pairs)
    coord_pairs.sort()
    for i in range(0,len(coord_pairs)):
        coord_pairs[i].append(i)
    
def read_connectivity(tbl_content, class_type):
    if blanks_exist(tbl_content):
        print('Table values must not be left blank')
        return 1 #Stop function execution
    ind_x1 = tbl_content[1].index('x1')
    ind_y1 = tbl_content[1].index('y1')
    ind_x2 = tbl_content[1].index('x2')
    ind_y2 = tbl_content[1].index('y2')
    ind_E = tbl_content[1].index('E')
    ind_A = tbl_content[1].index('A')
    trusses = []
    for i in range(2,len(tbl_content)): #content rows only
        x1 = tbl_content[i][ind_x1]
        y1 = tbl_content[i][ind_y1]
        x2 = tbl_content[i][ind_x2]
        y2 = tbl_content[i][ind_y2]
        E = tbl_content[i][ind_E]
        A = tbl_content[i][ind_A]            

def read_params(tbl_content, var_list):
    if blanks_exist(tbl_content):
        print('Table values must not be left blank')
        return 1 #Stop function execution
    for i in range(0,len(tbl_content)):
        for j in range(0,len(tbl_content[i])):
            for k in range(0,len(var_list)):
                if (tbl_content[i][j]==var_list[k].descript_name):
                    var_list[k].val=tbl_content[i+1][j]
                    print('Set ' + sim_params[k].descript_name +\
                            ' to ' + str(sim_tbl.content[i+1][j]))
                    
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
sim_params = [c,dof]

print('\n')
read_params(sim_tbl.content,sim_params)

for i in range(0,len(sim_params)):
    print(sim_params[i].descript_name)
    print(sim_params[i].val)
