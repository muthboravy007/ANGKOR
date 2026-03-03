PyReactor Benchmark - Bare UO2 Slab
c ========CELL CARD ==============
10 1 -3.82 -1 2 -3 4 -5 6 imp:n=1
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
m1   92235.80c  0.000304
     92238.80c  0.009504
     8016.80c   0.019408
     1001.80c   0.054400
     1002.80c   0.000008
mt1  lwtr.20t
kcode  20000  1.0  50  300
ksrc   0.0  0.0  0.0
       40.0 0.0  0.0
      -40.0 0.0  0.0
print