#include <stdio.h>
#include <stdlib.h>

typedef struct {
   float x;
   float y;
} Point;

Point get_point() {
   Point p = { 10.0, 20.0 };
   return p;
}

int main() {
   Point p = get_point();
   printf("%f %f\n", p.x, p.y);
   return 0;
}
