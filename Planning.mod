 /*********************************************
 Factory Planning Dima & Ori 2016
 *********************************************/

int D = ...; 
range deps = 1..D;
float Size[deps] = ...; 
float R[deps,deps] =...;
int Time = ...;
execute { cplex.tilim = Time}  ;

float AreaSum = sum(dep in deps) Size[dep];
 float MaxArea =max(dep in deps) Size[dep]; // biggest deparment
 float M = AreaSum*1.1/(sqrt(MaxArea)*0.7); // big M as the longest 1-dimentional distanse possible
 float w1 = ...;	// w1
 float w2 = 1-w1;   // w2
 float HugeM = 100000;  // for area only calculations


 dvar float+ yu[deps]; // upper coordinate
 dvar float+ yd[deps]; // lower
 dvar float+ xl[deps]; // left
 dvar float+ xr[deps]; // right
 dvar float+ yc[deps]; // center y
 dvar float+ xc[deps]; // center x
 dvar float+ distx[deps,deps]; // x distance
 dvar float+ disty[deps,deps]; // y distance
 dvar float+ tlx; // x total left
 dvar float+ trx; // x total right
 dvar float+ totx; // x total grid size
 dvar float+ tuy; // y total up
 dvar float+ tdy; // y total down
 dvar float+ toty; // y total grid size
 
 dvar boolean up[deps,deps]; // i have to be above j
 dvar boolean right[deps,deps]; // i have to be to the right of j

minimize w1*(sum(i in deps, j in deps) 0.5*R[i,j]*(distx[i,j]+disty[i,j])) + w2*sqrt(AreaSum)*(0.4*totx+0.6*toty) + HugeM*w2^HugeM*(0.2*totx+0.8*toty);
// all dist are manhattan
// all deps are rect
// instead of area we minimize ~perimeter

subject to {

forall(i in deps) xr[i]-xl[i] >= 0.701* (yu[i]-yd[i]); // 
forall(i in deps) xr[i]-xl[i] <= 1.299* (yu[i]-yd[i]); // 
forall(i in deps) 1.29*(xr[i]-xl[i]) >= (yu[i]-yd[i]); // 
forall(i in deps) 0.71*(xr[i]-xl[i]) <= (yu[i]-yd[i]); // 

forall(i in deps) (xr[i]-xl[i]) + (yu[i]-yd[i]) <= 2.085*sqrt(Size[i]); // 
forall(i in deps) (xr[i]-xl[i]) + (yu[i]-yd[i]) >= 1.915*sqrt(Size[i]); // 

forall(i in deps) xr[i]+xl[i] == 2*xc[i]; // center is the avg
forall(i in deps) yu[i]+yd[i] == 2*yc[i]; // ...


forall(i in deps,j in deps) xc[i]-xc[j] <= distx[i,j]; // dist is max diff between centers
forall(i in deps,j in deps) yc[i]-yc[j] <= disty[i,j]; //...
forall(i in deps,j in deps) distx[i,j] == distx[j,i]; // dist is cymmetric
forall(i in deps,j in deps) disty[i,j] == disty[j,i]; //...


forall(i in deps) xl[i] >= tlx; // the leftest coordinate is smaller than all x
forall(i in deps) xr[i] <= trx; // ... rightest   ...        bigger .....     x
forall(i in deps) yu[i] <= tuy; // ... upper      ...        bigger .....     y 
forall(i in deps) yd[i] >= tdy; // ... lower     ...        smaller .....     y

forall(i in deps,j in deps) yd[i] - yu[j] + M*(1-up[i,j]) >=0 ; // if up[i,j] -> yd[i] > yu[j]
forall(i in deps,j in deps) xl[i] - xr[j] + M*(1-right[i,j]) >=0 ; // if right[i,j] -> xl[i] > xr[j]
forall(i in deps,j in deps: i!=j) right[i,j]+up[i,j] + right[j,i]+up[j,i] == 1; // two deps do not overlap at least at one dimention

tlx == 0; // x reference point
tdy == 0; // y reference point
trx - tlx == totx; // grid x size
tuy - tdy == toty; // grid y size
totx >= toty; // symmetry break

};