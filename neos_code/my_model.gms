$offlisting
$offdigit

EQUATIONS
	c1
	c2_hi
	c3_hi
	c4_hi
	c5_hi
	c6_hi
	c7_hi
	c8_hi
	c9_hi
	c10_hi
	c11_hi
	c12_hi
	c13_hi
	c14_hi
	c15_hi
	c16_hi
	c17_hi
	c18_hi
	c19_hi
	c20
	c21
	c22
	c23
	c24
	c25
	c26;

INTEGER VARIABLES
	x1
	x2
	x3
	x4
	x5
	x6
	x7
	x8
	x9;

VARIABLES
	GAMS_OBJECTIVE
	;


c1.. x1*(x2*x3 - x4*x5) - x6*(x7*x3 - x4*x8) + x9*(x7*x5 - x2*x8) =e= 1386566 ;
c2_hi.. 1.1911764705882353*x6 - x1 =l= 0 ;
c3_hi.. x1 + (-1.1919999999999999)*x6 =l= 0 ;
c4_hi.. 1.5432098765432098*x9 - x6 =l= 0 ;
c5_hi.. x6 + (-1.5454545454545454)*x9 =l= 0 ;
c6_hi.. 1.8389261744966443*x9 - x1 =l= 0 ;
c7_hi.. x1 + (-1.8409090909090908)*x9 =l= 0 ;
c8_hi.. 1.1911764705882353*x2 - x7 =l= 0 ;
c9_hi.. x7 + (-1.1919999999999999)*x2 =l= 0 ;
c10_hi.. 1.5432098765432098*x4 - x2 =l= 0 ;
c11_hi.. x2 + (-1.5454545454545454)*x4 =l= 0 ;
c12_hi.. 1.8389261744966443*x4 - x7 =l= 0 ;
c13_hi.. x7 + (-1.8409090909090908)*x4 =l= 0 ;
c14_hi.. 1.1911764705882353*x5 - x8 =l= 0 ;
c15_hi.. x8 + (-1.1919999999999999)*x5 =l= 0 ;
c16_hi.. 1.5432098765432098*x3 - x5 =l= 0 ;
c17_hi.. x5 + (-1.5454545454545454)*x3 =l= 0 ;
c18_hi.. 1.8389261744966443*x3 - x8 =l= 0 ;
c19_hi.. x8 + (-1.8409090909090908)*x3 =l= 0 ;
c20.. x7 =e= 84605 ;
c21.. x2 =e= 71006 ;
c22.. x4 =e= 45992 ;
c23.. x8 =e= 71633 ;
c24.. x5 =e= 60130 ;
c25.. x3 =e= 38945 ;
c26.. GAMS_OBJECTIVE =e= 0 ;

x1.up = +1.0E+100;
x2.up = +1.0E+100;
x3.up = +1.0E+100;
x4.up = +1.0E+100;
x5.up = +1.0E+100;
x6.up = +1.0E+100;
x7.up = +1.0E+100;
x8.up = +1.0E+100;
x9.up = +1.0E+100;

MODEL GAMS_MODEL /all/ ;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;
SOLVE GAMS_MODEL USING minlp minimizing GAMS_OBJECTIVE;

Scalars MODELSTAT 'model status', SOLVESTAT 'solve status';
MODELSTAT = GAMS_MODEL.modelstat;
SOLVESTAT = GAMS_MODEL.solvestat;

Scalar OBJEST 'best objective', OBJVAL 'objective value';
OBJEST = GAMS_MODEL.objest;
OBJVAL = GAMS_MODEL.objval;

Scalar NUMVAR 'number of variables';
NUMVAR = GAMS_MODEL.numvar

Scalar NUMEQU 'number of equations';
NUMEQU = GAMS_MODEL.numequ

Scalar NUMDVAR 'number of discrete variables';
NUMDVAR = GAMS_MODEL.numdvar

Scalar NUMNZ 'number of nonzeros';
NUMNZ = GAMS_MODEL.numnz

Scalar ETSOLVE 'time to execute solve statement';
ETSOLVE = GAMS_MODEL.etsolve

