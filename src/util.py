################################################################################
# File     : util.py
# Function : General Utility Library
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

"""
General Utility functions

Rough Conventions:
Almost every one has an exception 

 - Predicates tend to end with p (e.g. evenp )
 - Functions starting with i tend to return iterators (e.g. iprimes )
 - Functions that use a predicate parameter MAY end in if (e.g. removeif)
"""

import time
import sys
import math
import traceback
import re
import functools
from functools import wraps

VERSION = "$Id$"

### Text Handling

def chomp( string ):
    """
    Perl-Like Chomp; strips line endings and returns just the string

    >>> chomp( "test\\n" )
    'test'

    @param string: string to chomp
    @return: string without ending newline
    """
    if string.endswith( '\r\n' ):
        return string[:-2]
    if string[-1] == '\r' or string[-1] == '\n':
        return string[:-1]
    return string

def chomplines( lst ):
    """
    Chomp useable with readlines()

    @param lst: list of strings to chomp
    @return: list of string without line endings
    """
    return [ chomp( item ) for item in lst ]

def istringcmp( string1, string2 ):
    """
    Case Insensitive String Cmp

    >>> istringcmp( "hello", "HELlo" )
    0

    @param string1: string to compare
    @param string2: string to compare
    @return:  0 if equal 1, < 0 if string2 greater, > 0 if string1 is greater

    """
    return cmp( string1.lower(), string2.lower() )

### List/Iterator functions
def unzip( iterables ):
    """
    Undo what zip does; Split a list of tuples into a tuple of lists where
    the first list is a list of all the first elements, second list is a 
    list of all second elements, etc.

    e.g. unzip a list of four-tuples into four lists

    >>>  unzip( [(1, 2, 3, 4), (3, 4, 5, 6), (10, 11, 12, 19)] )
    ([1, 3, 10], [2, 4, 11], [3, 5, 12], [4, 6, 19])


    @param iterables: iterable to unzip
    @return: tuple of lists
    """
    length = len( iterables[ 0 ] )
    result = [ [] for _ in xrange( length )]
    for item in iterables:
        for index, part in enumerate(item):
            result[ index ].append( part )
    return tuple( result )

def count( *iterables ):
    """
    count( *iterables )

    Count items in  iterables that eval to true; note this is different
    from the list method count which returns the count of values that
    are equal to a given reference.

    e.g.

    [0, None, '', [], {}, False] are all False

    >>> count( [0, None, '', [], {}, False] )
    0

    non-0 numbers are true as are non empty strings

    >>> count( [1, 2, 3, 4, 'hello'] )
    5

    @param iterables: one or more iterables to count over
    @return: count of items that are not False or equivalent

    """
    counter = 0
    for iterable in iterables:
        for i in iterable:
            if i:
                counter += 1
    return counter

def countif( pred, *iterables ):
    """
    countif( pred, *iterables )

    Apply predicate to iterables and count times when predicate is true.
    Would be equivalent to count( map( pred, *iterables ) ) if map
    took multiple list parameters

    >>> countif( evenp, range( 1, 5 ) )
    2

    @param pred: predicate to call on each item
    @returns: count of items that when result of pred( item ) is true

    """
    counter = 0
    for iterable in iterables:
        for i in iterable:
            if pred( i ):
                counter += 1
    return counter

def mapinto( fun, lst ):
    """
    mapinto(fun,lst)

    Same as map except modifies list in place

    >>> a = range( 0, 5 )
    >>> a
    [0, 1, 2, 3, 4]
    >>> mapinto( lambda x: x + 1, a )
    [1, 2, 3, 4, 5]
    >>> a
    [1, 2, 3, 4, 5]

    @param fun: function to call on each item in lst
    @param lst: list to map in place in
    @return: original list (note: not a copy)

    """
    if lst == None:
        return None
    for idx, val in enumerate( lst ):
        lst[ idx ] = fun( val )
    return lst

def partition( fun, iterable ):
    """
    partition( fun, iterable )

    Partition iterable into two sublists (a,b) where
    items in a are when f returns a True value
    items in b are when f returns a non-True value

    @param fun: function used to determine where to partition
    @returns: tuple ( a, b ) where a is all items satisifying pred fun and b
    where they don't
    """
    truep = []
    falsep = []
    for i in iterable:
        if fun( i ):
            truep.append( i )
        else:
            falsep.append( i )
    return ( truep, falsep )

def removeif( pred, lst ):
    """
    removeif( pred, lst )

    Remove all items where pred returns a true value

    @param pred: predicate to test each item
    @param lst: list to analyze
    @returns: None
    """
    todel = list( ipositions( [ pred( item ) for item in lst ] ) )
    for i in todel[::-1]:
        del lst[ i ]

def span( pred, iterable ):
    """
    span( pred, iterable )

    split iterable into two lists when pred first goes to a false value

    >>> span( evenp, [2,4,6,8,1,3,5,7] )
    ([2, 4, 6, 8], [1, 3, 5, 7])

    @param pred: predicate
    @param iterable: iterable to iterate over
    @returns: a tuple of lists
    """
    lst = list( iterable )
    for i, item in enumerate( lst ):
        if not pred( item ):
            return ( lst[0:i], lst[i:] )
    return ( lst, [] )

def brk( pred, iterable ):
    """
    brk( pred, iterable )

    split list into two lists when pred first goes to true

    >>> brk( oddp,[2,4,6,8,1,3,5,7] )
    ([2, 4, 6, 8], [1, 3, 5, 7])

    @param pred: predicate to call for each item
    @param iterable: iterable to break
    @returns: tuple of two lists

    """
    lst = list( iterable )
    for i, item in enumerate( lst ):
        if pred( item ):
            return ( lst[0:i], lst[i:] )
    return ( lst, [] )

def ipositions( iterable ):
    """
    Iterator that returns positions of items that are considered true by if

    e.g.
    
    Since none, False, 0 and '' are all considered False :

    >>> list( ipositions( [1,None,False,0,'',4] ) )
    [0, 5] 

    @param iterable: iterable
    @returns: generator
    """
    for idx, item in enumerate( iterable ):
        if item:
            yield idx

def iunique( iterable, hashfn = None ):
    """
    Returns unique items from an iterable.

    @param iterable: iterable
    @param hashfn: Hash function to use

    @returns: generator that returns unique items for an iterable
    """
    if not hashfn:
        hashfn = lambda x: x
    values = set( )
    for item in iterable:
        value = hashfn( item )
        if not value in values:
            values.add( value )
            yield item

def iterablep( obj ):
    """
    Check if object supports iter protocol
    
    @param obj: object to test
    @returns: True if item supports iter protocol
    """
    if getattr( obj, '__iter__', None ):
        return True
    return False

def iteratorp( obj ):
    """
    Check if is an iterator

    @param obj: object to test
    @returns: True if item is an iterator
    """
    if getattr( obj, '__iter__', None ) and getattr( obj, 'next', None ):
        return True
    return False

def first( arg ):
    """
    First function (as in lisp)
    
    Useful when supplied as first class function argument 

    @param arg: iterable
    @return: first item in iterable or None if not available
    """
    try:
        return arg[0]
    except:
        return None

### Util Functions

def compose( outerfun, innerfun ):
    """ 
    Compose two functinos 

    >>> f = compose( lambda x: x ** 2, lambda x: x + 4 )
    >>> f( 3 )
    49
    
    @param outerfun: function takes result of innerfunction as parameter 
    and provides return value of the composed function
    @param innerfun: function takes paramter of composed function and
    provides parameter for outerfunction
    @returns: composed function
    """
    def composedfun( *args, **kwords ):
        """
        Composition of two functions
        """
        return outerfun( innerfun( *args, **kwords ) )
    return composedfun

def identity( arg ):
    """
    return argument unmodified
    
    Useful when passed as a first class function.
    
    @param arg: any object
    @return: returns object without any modification
    """
    return arg

def memoize( func=None, keyfn=tuple ):
    """
    Memoize a function.  That is, in effect, cache the solution for
    a given set of parameters so future calls will just return the 
    value instead of running the computation again.

    The cache by default is keyed off the tuple of all parameters. 
    This behavior can overridden by providing a key function.
    The key function takes in a list of parameters and must compute
    a value that is hashable to store the solution.

    Important: 
    Both the key function and the underlying function must be idempotent 
    or otherwise memoization will not work properly.

    @param func: Function to memoize
    @param keyfn:  i.e. hash or discriminant function.  Result is stored in 
    dictionary and is used in comparisons to see if value is already cached
    @returns:  Wrapped function
    """
    if func != None:
        memo_table = {}
        @wraps( func )
        def memoized( *args ):
            """
            Memoized Function
            """
            value = keyfn( args )
            if value in memo_table:
                return memo_table[ value ]
            else:
                result = func( *args )
                memo_table[ value ] = result
                return result
        return memoized
    else:
        return functools.partial( memoize, keyfn = keyfn )

def log( prefix, msg, output=sys.stderr ):
    """
    Write a log message to output

    @param prefix: string to put in log specifying type of msg
    @param msg: message to log
    @param output: output stream to write to
    """
    fstr = "%.4f " % ( time.time() )
    if prefix != None:
        fstr +=  " %-5s " % ( prefix )
    fstr += " " + msg
    print  >> output, fstr
    
def trace( fun=None, prefix=None, output=sys.stdout ):
    """
    Decorator for a function that in effect generates a log event 
    every time a function is called. The log message contains the 
    function name, parameters, return value and timestamp.

    @param fun: function to trace
    @param prefix: prefix to supply in log
    """
    if fun != None:
        @wraps( fun )
        def call( *args, **kword ):
            """ 
            Call the function
            """
            # generate the message 
            msg = fun.func_name
            if len( args ) == 1 and len( kword ) == 0:
                msg += "( %s )" % (args)
            else:
                msg += "( "
                isfirst = True
                # fill out the normal arguments
                for item in args:
                    if not first:
                        msg += ", "
                    msg += str( args )
                    isfirst = False
                # fill out the keyword arguments                    
                for item in kword:
                    if not isfirst:
                        msg += ", "
                    msg += "%s = %s" % ( item, kword[ item ] )
                    isfirst = False                
                msg += " )"
            result = fun( *args, **kword )
            msg += " => %s" % (result)
            # log message
            log( prefix, msg, output=output )
            return result
        return call
    else:
        # if no function supplied; return a partial application with all
        # but the function applied
        return functools.partial( trace, prefix=prefix, output=output )

def logtrace( fun ):
    """
    Decorator that generates a log message everytime a function is called.
    This log function contains the 'LOG' string as its prefix.

    @param fun: function to trace
    @returns: wrapped function
    """
    return trace( fun, prefix="LOG" )

def clocked( fun, output = sys.stderr ):
    """
    Decorator that clocks a function each time it is called.

    @param fun: function to clock
    @param output: output stream to use
    @returns: a wrapped function
    """
    @wraps( fun )
    def call( *args, **kword ):
        """ 
        Call the function
        """
        msg = fun.func_name
        start = time.time()
        result = fun( *args, **kword )
        end = time.time()        
        msg += " (%.4f s)" % ( end - start)
        print >> output, msg 
        return result
    return call
    
def clock( fun, *args, **kword ):
    """
    Time a function

    @param fun: function to clock
    @param args: arguments for function
    @param kword: keyword arguments for function
    """
    start = time.time()
    try:
        result = fun( *args, **kword )
    except KeyboardInterrupt:
        print 'Interrupted'
        result = None
    end = time.time()
    print >> sys.stderr, "Clocked %f" % (end-start)
    return result

def warn( msg ):
    """
    Perl-like warn

    prints message to stderr with line number and filename if possible

    @param msg: message to print to stderr
    """
    (filename, lineno) = (None, None)
    suffix = ''
    frame = traceback.extract_stack(limit=1)
    if frame != []:
        (filename, lineno, _, _) = frame[0]
        suffix = "at %s %s" % (filename, lineno)
    print >> sys.stderr, msg, suffix

def die( msg ):
    """
    Perl-like Die
    
    prints message to stderr with line number and filename if possible
    then exits with error code.

    @param msg: message to print to stderr
    """
    (filename, lineno) = (None, None)
    suffix = ''
    frame = traceback.extract_stack(limit=1)
    if frame != []:
        (filename, lineno, _, _) = frame[0]
        suffix = "at %s %s" % (filename, lineno)
    print >> sys.stderr, msg, suffix
    sys.exit( 1 )

def grep( pattern, slist ):
    """
    Grep useful for input from readlines()

    Search for pattern in each string in slist.  Pattern is
    plain text.

    @param pattern: plain text pattern
    @param slist: list of strings
    @return: list of values where pattern exists in value
    """
    return [ txt for txt in slist if pattern in txt ]

def egrep( pattern, slist ):
    """
    Egrep useful for input from readlines()

    Search for pattern in each string in slist.  Pattern is
    plain text representation of a regexp.

    @param pattern: regular expression pattern in string form
    @param slist: list of strings
    @return: list of values where pattern exists in value
    """
    regexp = re.compile( pattern )
    return [ txt for txt in slist if regexp.match( txt ) ]

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
    return sum(lst)/float(len(lst))

def geometric_mean( lst ):
    """
    Geometric mean

    e.g.

    >>> geometric_mean( [ 2**3, 2**5, 2**8, 2**3, 2**1 ] )
    16.000000000000004
    
    @param lst: numbers to take the geometric mean of
    @returns: geometric mean
    """
    exp = (1/float(len(lst)))
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
        for item in xrange( 2, nval ):
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
    yield 0
    yield 1
    fib_n1 = 0
    fib_n2 = 1
    while True:
        result = fib_n1 + fib_n2
        fib_n1 = fib_n2
        fib_n2 = result
        yield result
