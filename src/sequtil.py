################################################################################
# File     : sequtil.py
# Function : Sequence Utility Library
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
