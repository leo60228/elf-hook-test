#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main(int argc, char **argv) {
  long int a = clock();
  printf("clock() = %ld\n", a);
  return 0;
}

