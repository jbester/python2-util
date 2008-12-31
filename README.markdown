Python-utility Library
=========================

Summary
-------

This library contains python native code to provide generic functionality
needed but not included in the standard library.  Majority of the 
library is composed of utility functions that provide functionality.  These
functions were pulled from multiple projects the author has written.  Secondly,
included is several decorators that provide functionality common in other
languages (e.g. memoize, function timing, and type annotations).

Packages
---------

 + pyutil.fnutil - Functional Utility
  + function composition
  + identity function
  + memoize
  + functions to measure timing

 + pyuil.mathutil - Math functions
  + derivative and integral functions
  + number theory functions
  + combinatorics (combinations, permutations etc)
  + general math functions (fibonnci, factorial, mean, etc)

 + pyutil.sequtil - lisp/scheme inspired sequence functions

 + pyutil.signature - Type checking decorator

 + pyutil.strutil - String functions
  + chomp
  + grep/egrep

 + pytuil.sysutil - system functions
  + logging
  + die/warn 
