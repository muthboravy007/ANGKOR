PyReactor Benchmark - Bare UO2 Slab
c ========CELL CARD ==============
10 1 -10.4 -1 2 -3 4 -5 6 imp:n=1
11 0       #10            imp:n=0

c ========SURFACE CARD ===========
1  px    80.0
2  px   -80.0
*3  py   1.0
*4  py  -1.0
*5  pz   1.0
*6  pz  -1.0

c =========Material and Data Card=
mode n
c f4:n 1
c e4 0.0 6.25e-7 20.0
c sd4 640.0
m1   92235.80c  0.01033
     92238.80c  0.32300
     8016.80c   0.66667
kcode  10000  1.0  50  200
ksrc   0.0  0.0  0.0
print