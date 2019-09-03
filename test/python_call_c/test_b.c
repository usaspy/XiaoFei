#include <stdio.h>  
#include <stdlib.h>  
#include "so_test.h"
int foo(int a, int b)  
{  
  printf("you input %d and %d\n", a, b);  
  return a*b;  
}  


float foo_float(float a,float b)
{
  return a*b;
}
