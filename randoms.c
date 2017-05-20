#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "randoms.h"

double rand_v(void)
{
  double v; // unitless
  v=((double)rand()/(double)RAND_MAX);
  printf("Random Poisson is %f\n",v);
  return v;
}

double rand_E(void)
{
  double E; // N/m^2 (Pa)
  double lin_dist, nonlin_dist;
  lin_dist=((double)rand()/(double)RAND_MAX); //0 to 1
  nonlin_dist=pow(lin_dist,10); //dist bias towards lower numbers
  double max_E=1*pow(10,12); // 1 TPa ~Young's Modulus of Diamond
  E=max_E*nonlin_dist;
  printf("Random elastic modulus is %f\n",E);
  return E;
}

double rand_stress(void)
{
  double stress; // N/m^2 (Pa)
  double lin_dist, nonlin_dist;
  lin_dist=((double)rand()/(double)RAND_MAX); //0 to 1
  nonlin_dist=pow(lin_dist,10); //dist bias towards lower numbers
  /* double max_stress=100*pow(10,9); // 100 TPa ~Tensile Strength of Diamond */
  double max_stress=10000; //temp for particular problem
  stress=max_stress*nonlin_dist;
  printf("Random stress is %f\n",stress);
  return stress;
}

double rand_strain(void)
{
  double strain; // unitless
  double lin_dist, nonlin_dist;
  lin_dist=((double)rand()/(double)RAND_MAX); //0 to 1
  nonlin_dist=pow(lin_dist,10); //dist bias towards lower numbers
  /* double max_strain=0.002; // Plastic deformation defined at ~0.2% */
  double max_strain=1.0; //temp for specific problem
  strain=max_strain*nonlin_dist;
  printf("Random strain is %f\n",strain);
  return strain;
}
