# Factory Planning Project (TAU 2015)


![alt text](https://github.com/dimgold/Factory_Planning/blob/master/png/905.png "Solution for biggest problem")


The goal of the project is given a projected set of departments and their areas, to plan the best arrangement that uses the smallest area keep short distances between related departments.
The full problem is NP-Hard, and a approximization approach was presented.

### The presented problem is:

Place n departments, with area given by a vector - A (10% deviance is allowed)
* Symmetric relation between department is given in Rij Matrix
* Relations are scaled between 0 (uninportant) and 3 (important to be located nearby)
* The distance is measured as rectangular distance (L1 norm) between the centers of the departments
* Goal Function is:

**Minimize [ w1 x Sumall_ij(Dij x Rij) + w2 x A]**

Where A is the area of minimal blocking rectangle of the whole factory, w1/w2 are input weights, R is the relation matrix and D is the distance matrix

Subject to restrictions:
* The ratio of blocking rectangle area compared to department area won't exceed 1.3
* The ratio of blocking rectangle sides of each department won't exceed 1.3

The solution approach used Python and CPLEX OPL MILP programming to reach the best planning.

### Files and Directories:
* resplot.py - main python code to generate the OPL input file, run the optimization and create the output image and data
* Planning.mod - main OPL code
* input.dat - OPL data input template
* inputs - folder with  10 problems x3 (w1=0/0.5/1) in xlsx accompanied with generated OPL dat file
* png - folder with result outline images
* txt  -folder with result metrics and coordinates

### Mixed Integer Linear Programming Model:

![alt text](https://github.com/dimgold/Factory_Planning/blob/master/png/linmodel.JPG "Linear Programming")
