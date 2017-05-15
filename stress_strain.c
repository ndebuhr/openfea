/************************************************

Neal DeBuhr
Calculates unknown properties for a
stress-strain element.

*************************************************/ 

#include <stdio.h>
#include <string.h>
#define STR_LEN 255
#define NUM_VARS 5

void assign_vals(double * var_ptrs[NUM_VARS], char unknown, char vars[NUM_VARS][2][255]);
static double * make_constitutive(double E, double v);

int main (void)
{
  // Programming variables
  char vars[NUM_VARS][2][255]={{"x","sigma_x"},{"y","sigma_y"},{"z","sigma_z"},{"E","Modulus of Elasticity"},{"v","Poisson's Ratio"}};
  char unknown;
  int i;
  // Solid mechanics variables
  double x, y, z, E, v;
  double * var_ptrs[NUM_VARS]={&x,&y,&z,&E,&v};
  
  printf(" INDEX | NAME\n");
  for (i=0; i<NUM_VARS; i++)
    printf("   %c   | %s\n",vars[i][0][0],vars[i][1]);

  printf("\nPlease specify the unknown variable: ");
  unknown=getchar();
  while (getchar()!='\n'); //clear residual stdin buffer chars

  assign_vals(var_ptrs,unknown,vars);
  
  switch (unknown) {
  case 'x' :
    x=1;
    break;
  case 'y' :
    y=1;
    break;
  case 'z' :
    z=1;
    break;
  case 'E' :
    E=1;
    break;
  case 'v' :
    v=1;
    break;
  }
    
  printf("%f\n%f\n%f\n%f\n%f\n",x,y,z,E,v);
  
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

static double * make_constitutive(double E, double v)
{
  int i;
  int j;
  double factor;
  static double constitutive[3][3];

  constitutive[0][0]=1-v;
  constitutive[1][0]=v;
  constitutive[0][1]=v;
  constitutive[1][1]=1-v;
  constitutive[2][2]=0.5-v;
  //leaves four elements at 0, as intended
  
  factor=E/((1+v)*(1-2*v));
  for (i=0; i<3; i++)
    {
      for (j=0; j<3; j++)
	{
	  constitutive[i][j]=constitutive[i][j]*factor;
	}
    }
  return constitutive;
}
