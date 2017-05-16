/****************************************

Neal DeBuhr
Calculates unknown properties for a
stress-strain element.
Assumes isotropic material properties

****************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define STR_LEN 255
#define NUM_VARS 14

void assign_vals(double * var_ptrs[NUM_VARS], char unknown, char vars[NUM_VARS][2][255]);
void make_stiffness(double E, double v, double stiffness[][6]);
int get_unknown_ind(char vars[NUM_VARS][2][255], char unknown);
double rand_v(void);
double rand_E(void);
double rand_stress(void);
double rand_strain(void);

int main (void)
{
  // Programming variables
  char vars[NUM_VARS][2][255]={{"A","Normal Stress in X"},{"B","Normal Stress in Y"},{"C","Normal Stress in Z"},
			       {"D","Shear Stress XY"},{"E","Shear Stress YZ"},{"F","Shear Stress XZ"},
			       {"G","Normal Strain in X"},{"H","Normal Strain in Y"},{"I","Normal Strain in Z"},
			       {"J","Shear Strain in XY"},{"K","Shear Strain in YZ"},{"L","Shear Strain in XZ"},
			       {"M","Modulus of Elasticity"},{"N","Poisson's Ratio"}};
  char unknown;
  int unknown_ind;
  int i;
  int j;
  int r_ind;
  // Solid mechanics variables
  double sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_xz, epsilon_x, epsilon_y, epsilon_z, gamma_xy, gamma_yz, gamma_xz, E, v;
  double * var_ptrs[NUM_VARS]={&sigma_x,&sigma_y,&sigma_z,
			       &tau_xy,&tau_yz,&tau_xz,
			       &epsilon_x,&epsilon_y,&epsilon_z,
			       &gamma_xy,&gamma_yz,&gamma_xz,
			       &E,&v};
  double (*fptr_v)(void)=&rand_v;
  double (*fptr_E)(void)=&rand_E;
  double (*fptr_stress)(void)=&rand_stress;
  double (*fptr_strain)(void)=&rand_strain;
  double (*fptr[4])(void)={fptr_v,fptr_E,fptr_stress,fptr_strain};
	  
  printf(" INDEX | NAME\n");
  for (i=0; i<NUM_VARS; i++)
    printf("   %c   | %s\n",vars[i][0][0],vars[i][1]);

  printf("\nPlease specify the unknown variable (type the index only): ");
  unknown=getchar();
  while (getchar()!='\n'); //clear residual stdin buffer chars

  switch (unknown) {
  case 'A' :
  case 'B' :
  case 'C' :
  case 'D' :
  case 'E' :
  case 'F' :
    r_ind=2; //use stress-style rand
    break;
  case 'G' :
  case 'H' :
  case 'I' :
  case 'J' :
  case 'K' :
  case 'L' :
    r_ind=3; //use strain-style rand
    break;
  case 'M' :
    r_ind=1; //use elasticity-style rand
    break;
  case 'N' :
    r_ind=0; //use poisson-style rand
    break;
  default :
    printf("Index not valid\n");
    return 0;
  }
  
  unknown_ind=get_unknown_ind(vars,unknown);
  assign_vals(var_ptrs,unknown,vars);

  // TODO - non-comically-primitive numerical methods
  double stiffness[6][6];
  for (i=0; i<10; i++); // blind guesses, then select best of the guesses
  {
    *var_ptrs[unknown_ind]=(*fptr[r_ind])(); //pulls the right random num
    make_stiffness(E,v,stiffness);
  }

  // Print stiffness matrix
  for (i=0; i<6; i++)
    {
      for (j=0; j<6; j++)
	{
	  if ((j+6*i+1)%6==0)
	    printf("%f\n",stiffness[i][j]);
	  else
	    printf("%f ",stiffness[i][j]);
	}
    }
  
  return 0;
}

void assign_vals(double * var_ptrs[NUM_VARS], char unknown, char vars[NUM_VARS][2][255])
{
  int i;
  
  for (i=0; i<NUM_VARS; i++)
    {
      if (unknown != vars[i][0][0])
	{
	  printf("Please provide a value for %s:",vars[i][1]);
	  scanf("%lf",var_ptrs[i]);
	  while (getchar()!='\n'); //clear residual stdin buffer chars
	}
    }
}

void make_stiffness(double E, double v, double stiffness[][6])
{
  int i;
  int j;
  double factor;

  //Set diagonal elements
  stiffness[0][0]=1-v;
  stiffness[1][1]=1-v;
  stiffness[2][2]=1-v;
  stiffness[3][3]=1-2*v;
  stiffness[4][4]=1-2*v;
  stiffness[5][5]=1-2*v;

  //Set non-diagonal elements
  stiffness[1][0]=v;
  stiffness[0][1]=v;
  stiffness[2][0]=v;
  stiffness[0][2]=v;
  stiffness[1][2]=v;
  stiffness[2][1]=v;
  
  factor=E/((1+v)*(1-2*v));
  /* factor=1; */ //for debug
  for (i=0; i<3; i++)
    {
      for (j=0; j<3; j++)
	{
	  stiffness[i][j]=stiffness[i][j]*factor;
	}
    }
}

int get_unknown_ind(char vars[NUM_VARS][2][255], char unknown)
{
  int i;

  for (i=0; i<NUM_VARS; i++)
    {
      if (unknown == vars[i][0][0])
	return i;
    }
}

double rand_v(void)
{
  double v; // unitless
  v=((double)rand()/(double)RAND_MAX);
  return v;
}

double rand_E(void)
{
  double E; // N/m^2 (Pa)
  double max_E=1*10^12; // 1 TPa ~Young's Modulus of Diamond
  E=max_E*((double)rand()/(double)RAND_MAX);
  return E;
}

double rand_stress(void)
{
  double stress; // N/m^2 (Pa)
  double max_stress=100*10^9; // 100 TPa ~Tensile Strength of Diamond
  stress=max_stress*((double)rand()/(double)RAND_MAX);
  return stress;
}

double rand_strain(void)
{
  double strain; // unitless
  double max_strain=0.002; // Plastic deformation defined at ~0.2%
  strain=max_strain*((double)rand()/(double)RAND_MAX);
  return strain;
}
