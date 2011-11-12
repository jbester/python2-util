################################################################################
# File     : mathutil.py
# Function : Math Utility Library
################################################################################
# Newest version can be obtained at http://www.freshlime.org
# Send comments or questions to code at freshlime dot org
################################################################################
# Copyright (c) 2008, J. Bester
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The name of the authors names of its contributors may be used to 
#       endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

from __future__ import division
import math

### Math Functions

def derivative( fun, xval = None, hval = (1e-8) ):
    """ 
    derivative( fun, xval = None, hval = (1e-8) ):

    Performs classical defintion of derivative [f(x+h)-f(x)]/h
    fun must be continuous around xval
    
    Returns the derivative of a function (fn):

    if the second parameter (xval) is given it returns the numeric derivative
    if there is no second parameter (xval) it returns a function which when
    given a parameter will evaluate to the numeric derivative of the function

    h can be specified even if xval is not and the derivative will be computed
    with that hval.

    @param fun: function to take derivative of
    @param xval: x position to take derivative at
    @param hval: epsilon value to use in calculation of derivative
    @returns: numerical derivative
    """
    if xval == None:
        def dfn( xval ):
            """
            Deriviative closure around a functionx
            """
            return derivative( fun , xval, hval )
        return dfn
    else:
        return ( fun( xval + hval ) - fun( xval ) )/hval

def integral( fun, xstart = None, xend = None, epsilon = (1e-3) ):
    """ 
    integral( fun, xstart = None, xend = None, hval = (1e-3) ):

    Performs classical definite integral using the trapezoid rule
    fun must be continuous over integrated intervals

    if either xstart or xend are not specified:
    
    a function is returned with the signature of 
    ifun( start = xstart, end  = xend, hval = epsilon )
    that is any arguments provided are default values ot the returned function
    
    otherwise:
    
    Returns the integral of a function (fn):

    @param fun: function to integrate
    @param xstart: x-position to start integration at
    @param xend: x-position to end integration at
    @param epsilon: x-size of each slice 
    @returns: numeric integral
    """
    if xstart == None or xend == None:
        def ifun( start = xstart, end  = xend, hval = epsilon ):
            """
            integral closure around a function
            """
            return integral( fun, start, end, hval )
        return ifun
    else:
        xval = xstart
        # sum of  .5 * (h( x ) = h( x + epsilon )) * epsilon
        area = 0
        while xval <= xend:
            area += .5 * (fun( xval ) + fun( xval + epsilon ))
            xval += epsilon
        area *= epsilon
        return area

def product( items, initial=1 ):
    """
    Product of paramter (must be iterable)
    
    >>> product( xrange( 1, 10 ) )
    362880

    @param items: one or more iterable items or numbers
    @returns: product of numbers
    """
    prod = initial
    for item in items:
        prod *= item
    return prod

def mean( lst ):
    """
    Arithmetic mean

    @param lst: numbers to take the mean of
    @returns: mean
    """
    return sum(lst)/len(lst)

def geometric_mean( lst ):
    """
    Geometric mean

    e.g.

    >>> geometric_mean( [ 2**3, 2**5, 2**8, 2**3, 2**1 ] )
    16.000000000000004
    
    @param lst: numbers to take the geometric mean of
    @returns: geometric mean
    """
    exp = (1/len(lst))
    prod = product(lst)
    return prod ** exp

def factorial( nval ):
    """ 
    Factorial

    @param nval: factorial to compute
    @returns: factorial of value
    """
    if nval <= 0:
        return 1
    else:
        # try to cut down the number of large multiplications
        # use a ring buffer to multiply
        ring_size = 20
        prod = [1] * ring_size
        idx = 0
        for item in xrange( 2, nval + 1 ):
            prod[ idx ] *= item
            idx = (idx + 1) % ring_size
        return product( prod )

def naive_primep( xval ):
    """
    Do a simple naive prime test (trial division)

    @param xval: value to test
    @returns: True if prime
    """
    if xval == 2:
        return True
    if xval % 2 == 0:
        return False
    j = 2
    # intentionally while loop instead of for w/ xrange to properly handle
    # fractional parts of roots
    while j <= math.sqrt( xval ):
        if xval % j == 0:
            return False
        j += 1
    return True

def gcd( aval, bval ):
    """ 
    Greatest Common Denominator

    Euclid's algorithm

    GCD(A,B)=GCD(B,A % B)

    @returns: Greatest common demonitor of both values
    """
    while bval != 0:
        temp = aval % bval
        aval = bval
        bval = temp
    return aval
    
def lcm( aval, bval ):
    """
    Lowest Common Multiple 

    LCM = a * b / GCD

    @returns: lowest common multiple of both values
    """
    return aval * bval  / gcd( aval, bval )

def naive_factor( nval ):
    """
    Naively factor an integer and return the set of factors

    @param nval: value to factor
    @returns: set of factors for value
    """
    result = set()
    root = int( math.sqrt( nval ) )
    if int(root) == root:
        root = int(root) + 1
    for i in range( 2, root ):
        # check if a multiple
        if nval % i == 0:
            result.add( i )
            result.add( nval / i )
    return result

def permutation( nval, rval ):
    """
    Permutation: ordered selection r of n

    n!/(n -r)!

    @param nval: total number of values
    @param rval: number of items to take at a time
    @returns: numbered of ordered combinations
    """
    return factorial( nval )/factorial( nval - rval )

def combination( nval, rval ):
    """
    Combination: unordered selection r of n

    n!/(r! * (n -r))!

    @param nval: total number of values
    @param rval: number of items to take at a time
    @returns: numbered of unordered combinations
    """
    return factorial( nval )/(factorial( rval ) * factorial( nval - rval ))

def combinations_with_repetition( nval, rval ):
    """
    Combination with repetition: Unordered selection r of n with repetition
    
    nCr( n + r - 1, r )

    @param nval: total number of values
    @param rval: number of items to take at a time
    @returns: numbered of uncombinations with replacement
    """
    return combination( nval + rval - 1, rval )
    
def iprimes( limit = None ):
    """
    Generator of primes using sieve of eratosthenes

    Number of composites stored in memory is equal to the number
    of primes found so far (i.e. the pi function approx x/log(x))

    @param limit: the upper limit on primes returned i.e. iprimes( 10 ) returns 
    a generator that will return each prime less than 10

    """
    # In essence this function keeps a rolling buffer of composites
    # based off the primes found so far

    # map of composite to their prime root
    composites = {} 
    # yield first prime not used below due to no other odd primes
    yield 2 
    number = 3
    # limit is used to obtain xrange like functionality
    while limit == None or number < limit:
        if number not in composites: # is prime
            yield number
            # find and store  next available odd composite
            # from the prime found
            candidate = 2 * number
            while candidate in composites or candidate % 2 == 0:
                candidate += number
            composites[ candidate ] = number
        else:
            prime = composites[ number ]
            del composites[ number ]
            # find and store the next available odd composite
            # from the prime factor
            candidate = number + prime
            while candidate in composites or candidate % 2 == 0:
                candidate += prime
            composites[ candidate ] = prime
        # skip even number
        number += 2

def evenp( val ):
    """ 
    Even predicate 

    @param val: value to test
    @returns: true if val is even
    """
    return val % 2 == 0

def oddp( val ):
    """ 
    Odd predicate 

    @param val: value to test
    @returns: true if val is odd
    """
    return val % 2 == 1

def ordered_combinations( data, size ):
    """
    Get all ordered combinations (aka permutations) of the data
    for the given size

    >>> ordered_combinations( ['a','b','c'], 2 )
    [['a', 'b'], ['a', 'c'], ['b', 'a'], ['b', 'c'], ['c', 'a'], ['c', 'b']]

    @param data: list of values
    @param size: size of combinations must be less than or equal to the 
    length of data
    @returns: list of ordered combinations
    """
    if size == 1:
        return [[item] for item in data]
    else:
        result = []
        # find all combinations of size - 1 for each subset
        # then add the missing item to create combinations of intended size 
        for idx, val in enumerate( data ):
            subset = data[ 0:idx ] + data[ idx+1: ]
            for subcombinations in ordered_combinations( subset, size - 1 ):
                result.append( [val] + subcombinations )
        return result

def unordered_combinations( data, size ):
    """
    Get all unordered combinations (aka combinations) of the data
    for the given size.

    >>> unordered_combinations( ['a','b','c'], 2 )
    [['a', 'b'], ['a', 'c'], ['b', 'c']]

    @param data: list of values
    @param size: size of combinations must be less than or equal to the 
    length of data
    @returns: list of unordered combinations

    """
    def __unordered( data, size ):
        """
        do an unordered combination of all items.

        Note: all items must be unique to properly work
        """
        if size == 1:
            return [[item] for item in data]
        else:
            result = []
            for idx, val in enumerate( data ):
                subset = data[ 0:idx ] + data[ idx + 1: ]
                for subcombinations in __unordered( subset, size - 1 ):
                    comb = [ val ] + subcombinations
                    # guaranteed to work since items are indicies
                    comb.sort()
                    # if indicies of a combination not in results add them
                    if comb not in result:
                        result.append( comb )
            return result
    # get unordered combinations of the indices
    result = __unordered( range( len( data )), size )
    # convert back to data items
    result = [[data[ part ] for part in item] for item in result ]
    return result

def fibonacci( term ):
    """
    Fibonacci for a single term

    Uses Djikstra's recursion

    F(2n) = (2 F(n-1) + F(n)) * F(n)

    F(2n-1) = F(n-1)^2 + F(n)^2

    @param term: term to return value for
    @returns: term in fibonacci sequence
    """
    # initial terms
    if term == 0:
        return 0
    if term == 1:
        return 1
    if term % 2 == 0:
        limit = term / 2
    else:
        limit = (term + 1) / 2
    val1 = 0
    val2 = 1
    pos = 2
    # perform recurance
    while pos <= limit:
        result = val1 + val2
        val1 = val2
        val2 = result
        pos += 1
        
    if term % 2 == 0:
        return (2 * val1 + (val2)) * (val2)
    else:
        return (val1 * val1 + val2 * val2 )

def ifibonacci( ):
    """
    Fibonacci series

    F(0) = 0

    F(1) = 1

    F(n) = F(n - 1) + F(n - 2)

    @returns: generator of terms in the fibonacci sequence
    """
    # initial terms
    yield 0
    yield 1
    fib_n1 = 0
    fib_n2 = 1
    # recurrance
    while True:
        result = fib_n1 + fib_n2
        fib_n1 = fib_n2
        fib_n2 = result
        yield result
