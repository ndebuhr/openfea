#define STR_LEN 255
#define NUM_VARS 14
#define NUM_UNKNOWNS 5
#define STIFFNESS_SIZE 6

void assign_vals(double * var_ptrs[NUM_VARS], char unknown[], char vars[NUM_VARS][2][STR_LEN]);
void make_stiffness(double E, double v, double stiffness[][6]);
int get_unknown_ind(char vars[NUM_VARS][2][STR_LEN], char unknown);
double get_err(double stiffness[][6],double * var_ptrs[NUM_VARS]);
double rand_v(void);
double rand_E(void);
double rand_stress(void);
double rand_strain(void);
int rand_index(char unknown);
