/****************************************

Neal DeBuhr
Calculates unknown properties for a
stress-strain element.

****************************************/

#include <stdio.h>
#include <string.h>
#define STR_LEN 255
#define NUM_VARS 14

void assign_vals(double * var_ptrs[NUM_VARS], char unknown, char vars[NUM_VARS][2][255]);
void populate_stiffness(double E, double v, double * stiffness);
int get_unknown_ind(double * var_ptrs[NUM_VARS], char unknown);
  
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
  // Solid mechanics variables
  double sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_xz, epsilon_x, epsilon_y, epsilon_z, gamma_xy, gamma_yz, gamma_xz, E, v;
  double * var_ptrs[NUM_VARS]={&sigma_x,&sigma_y,&sigma_z,
			       &tau_xy,&tau_yz,&tau_xz,
			       &epsilon_x,&epsilon_y,&epsilon_z,
			       &gamma_xy,&gamma_yz,&gamma_xz,
			       &E,&v};
  
  printf(" INDEX | NAME\n");
  for (i=0; i<NUM_VARS; i++)
    printf("   %c   | %s\n",vars[i][0][0],vars[i][1]);

  printf("\nPlease specify the unknown variable (type the index only): ");
  unknown=getchar();
  while (getchar()!='\n'); //clear residual stdin buffer chars

  unknown_ind=get_unknown_ind(var_ptrs,unknown);
  assign_vals(var_ptrs,unknown,vars);

  for (i=0; i<1000000; i++); //guess, no check
  {
    var_ptrs[unknown_ind]=((double)rand()/(double)RAND_MAX); //not uniform, but okay
    // TODO Finish loop and fix 0-1 rand to proper range based on variable type
    double stiffness[6][6];
    populate_stiffness(E,v,stiffness);
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

void populate_stiffness(double E, double v, double * stiffness)
{
  int i;
  int j;
  double factor;

  stiffness[0][0]=1-v;
  stiffness[1][0]=v;
  stiffness[0][1]=v;
  stiffness[1][1]=1-v;
  stiffness[2][2]=0.5-v;
  //leaves four elements at 0, as intended
  
  factor=E/((1+v)*(1-2*v));
  for (i=0; i<3; i++)
    {
      for (j=0; j<3; j++)
	{
	  stiffness[i][j]=stiffness[i][j]*factor;
	}
    }
  return stiffness;
}

int get_unknown_ind(double * var_ptrs[NUM_VARS], char unknown)
{
  int i;

  for (i=0; i<NUM_VARS; i++)
    {
      if (unknown == vars[i][0][0])
	return i;
    }
}
