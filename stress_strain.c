/****************************************

Neal DeBuhr
Calculates unknown properties for a
stress-strain element.
Assumes isotropic material properties

TODO: Finish calculation engine and
include auxiliary calculations (eg.
Von Mises stress, principle stresses,
etc.)

****************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>
#include <float.h>
#include <time.h>
#include "stress_strain.h"
#include "randoms.h"

int main (int argc, char * argv[])
{
  clock_t begin = clock();
  // Programming variables
  char vars[NUM_VARS][2][STR_LEN]={{"A","Normal Stress in X"},{"B","Normal Stress in Y"},{"C","Normal Stress in Z"},
			       {"D","Shear Stress XY"},{"E","Shear Stress YZ"},{"F","Shear Stress XZ"},
			       {"G","Normal Strain in X"},{"H","Normal Strain in Y"},{"I","Normal Strain in Z"},
			       {"J","Shear Strain in XY"},{"K","Shear Strain in YZ"},{"L","Shear Strain in XZ"},
			       {"M","Modulus of Elasticity"},{"N","Poisson's Ratio"}};
  char unknown;
  int unknown_ind;
  int i;
  int j;
  int r_ind[NUM_UNKNOWNS];
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
  char unknowns[NUM_UNKNOWNS];
  int unknown_inds[NUM_UNKNOWNS];
  
  printf(" INDEX | NAME\n");
  for (i=0; i<NUM_VARS; i++)
    printf("   %c   | %s\n",vars[i][0][0],vars[i][1]);

  printf("%d\n",argc);
  if (argc==1)
    {
      for (i=0; i<NUM_UNKNOWNS; i++)
	{
	  printf("\nPlease specify the unknown variable %d (type the index only): ",i+1);
	  unknowns[i]=getchar();
	  while (getchar()!='\n'); //clear residual stdin buffer chars
	  
	  r_ind[i]=rand_index(unknowns[i]);
	  unknown_inds[i]=get_unknown_ind(vars,unknowns[i]);
	}
    }
  else
    {
      for (i=0; i<NUM_UNKNOWNS; i++)
	{
	  unknowns[i]=argv[1][i];
	  r_ind[i]=rand_index(unknowns[i]);
	  unknown_inds[i]=get_unknown_ind(vars,unknowns[i]);
	}
    }

  assign_vals(var_ptrs,unknowns,vars);  

  // TODO - non-comically-primitive numerical methods
  double stiffness[STIFFNESS_SIZE][STIFFNESS_SIZE];
  double prev_err;
  double err;
  double soln_conv[NUM_UNKNOWNS];
  for (i=0; i<10000000; i++) // blind guesses, then select best of the guesses
  {
    for (j=0;j<NUM_UNKNOWNS;j++)
      *var_ptrs[unknown_inds[j]]=(*fptr[r_ind[j]])(); //pulls the right random num
    make_stiffness(E,v,stiffness);
    err=get_err(stiffness,var_ptrs);
    if (i==0)
      {
	prev_err=err;
	for (j=0; j<NUM_UNKNOWNS; j++)
	  soln_conv[j]=*var_ptrs[unknown_inds[j]];
      }
    if (prev_err>err)
      {
	for (j=0; j<NUM_UNKNOWNS; j++)
	  soln_conv[j]=*var_ptrs[unknown_inds[j]];
	prev_err=err;
      }
    printf("%f - %f - %f - %f\n",soln_conv[0],*var_ptrs[unknown_inds[0]],prev_err,err);
  }

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("Minutes spent: %f\n",time_spent/60);
  
  return 0;
}

void assign_vals(double * var_ptrs[NUM_VARS], char unknown[], char vars[NUM_VARS][2][STR_LEN])
{
  int i;
  int j;
  bool is_known;
  
  for (i=0; i<NUM_VARS; i++)
    {
      is_known=true;
      for (j=0; j<NUM_UNKNOWNS; j++)
	if (unknown[j] == vars[i][0][0])
	  is_known=false;
      if (is_known)
	{
	  printf("Please provide a value for %s:",vars[i][1]);
	  scanf("%lf",var_ptrs[i]);
	  while (getchar()!='\n'); //clear residual stdin buffer chars
	}
    }
}

void make_stiffness(double E, double v, double stiffness[][STIFFNESS_SIZE])
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

int get_unknown_ind(char vars[NUM_VARS][2][STR_LEN], char unknown)
{
  int i;

  for (i=0; i<NUM_VARS; i++)
    {
      if (unknown == vars[i][0][0])
	return i;
    }
}

double get_err(double stiffness[][STIFFNESS_SIZE],double * var_ptrs[NUM_VARS])
{
  int i;
  int j;
  double l_side, r_side;
  double mag_avg;
  double err_cont;
  double err_sqr;
  double err_sqr_total;
  //stress vector
  double stress[STIFFNESS_SIZE]={*var_ptrs[0],*var_ptrs[1],*var_ptrs[2],
		    *var_ptrs[3],*var_ptrs[4],*var_ptrs[5]};
  double strain[STIFFNESS_SIZE]={*var_ptrs[6],*var_ptrs[7],*var_ptrs[8],
		    *var_ptrs[9],*var_ptrs[10],*var_ptrs[11]};
  err_sqr_total=0;
  for (i=0; i<STIFFNESS_SIZE; i++)
    {
      l_side=stress[i];
      r_side=0;
      for (j=0; j<STIFFNESS_SIZE; j++)
	r_side+=stiffness[i][j]*strain[j];
      printf("%10f - %10f\n",l_side,r_side);
      mag_avg=(fabs(l_side)+fabs(r_side))/2;
      err_cont=(fabs(l_side-r_side))/mag_avg; //normalize error with magnitude
      if (isnan(err_cont))
	err_cont=0; //resolves divide by 0 if no error
      err_sqr_total+=err_cont*err_cont;
    }
  if (isnan(err_sqr_total))
    err_sqr_total=DBL_MAX; //ceiling on error
  return err_sqr_total;
}

int rand_index(char unknown)
{
  int r_ind;
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
  }
  
  return r_ind;
}
