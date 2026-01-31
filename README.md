# Programming-Assignment-1-Matching-and-Verifying
Students

Boluwatife “Bolu” Abegunde UFID: 67949259
Varun Yelchur UFID: 73222847

Task C:
The Gale-Shapley algorithm from the code was benchmarked with the sizes given in the example: 1,2,4,8,16,32,64,128,256,512. The graph labeled "gmpartc.png" shows this relationship. This shows that the runtime increases as n also increases. This is O(n^2) because in one scenario, each hospital could propose to all students. (R was used for this graph, the csv and rmd are also attached: this is located in PartCExtras)

To run Part B(verifier), the preferences file is redirected into the program, while the matching to be checked is specified after the script name. The command python3 src/verify.py tests/output.out < tests/test.in runs the verifier on the preferences in tests/test.in and checks whether the matching in tests/output.out is both valid and stable.

To run Part A:
The command: python3 src/galematching.py < tests/test.in is used. This means the file for Task A galematching.py is run against the input in test.in. If a different input file needs to be used, then that second argument is altered.


Graph:
The graph compares the running time of two programs as the problem size increases:
Matcher(circles) — Gale–Shapley  algorithm
Verifier(triangles) — validity & stability checker

The x-axis shows the number of hospitals/students, and the y-axis shows the execution time in seconds.

Observed Trend: Both curves rise slowly at first and then increase more rapidly as n grows. The shape of both lines is curved upward, not straight. This indicates that the runtime growth is quadratic.
