from utils import write_csv_rows, read_csv_rows

class input_table:
    def __init__(self, filename, name, headers, content=[]):
        self.filename = filename
        self.name = name
        self.headers = headers
        self.content = content

connect_filename = 'connectivity.csv'
connect_name = ['Connectivity Table']
connect_headers = ['x1','y1','x2','y2','E','A']
connect_tbl = input_table(connect_filename,
                          connect_name,
                          connect_headers)

force_filename = 'forces.csv'
force_name = ['Force Table']
force_headers = ['x','y','Fx','Fy']
force_tbl = input_table(force_filename,
                        force_name,
                        force_headers)

bc_filename = 'boundary_conditions.csv'
bc_name = ['Boundary Conditions']
bc_headers = ['x','y','Constrained Dimension','Displacement']
bc_tbl = input_table(bc_filename,
                     bc_name,
                     bc_headers)

sim_filename = 'simulation_parameters.csv'
sim_name = ['Simulation Parameters']
sim_headers = ['Numerical Soln Multiplier','Degrees of Freedom']
sim_content = ['1e9']
sim_tbl = input_table(sim_filename,
                      sim_name,
                      sim_headers,
                      sim_content)

input_files = [connect_tbl,force_tbl,bc_tbl,sim_tbl]

for i in range(0,len(input_files)):
    tbl_list = [input_files[i].name,
                input_files[i].headers,
                input_files[i].content]
    write_csv_rows(input_files[i].filename,tbl_list)
    print(input_files[i].name[0] + ' written to ' +\
          input_files[i].filename)
