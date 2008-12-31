################################################################################
# File     : fnutils.py
# Function : Function Utility Library
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

import functools
import time
import sys

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
        @functools.wraps( func )
        def memoized( *args ):
            """
            Memoized Function
            """
            value = keyfn( args )
            # check if parameter is in memo table
            # if so return cached value
            if value in memo_table:
                return memo_table[ value ]
            else:
                # if not in table store in table
                result = func( *args )
                memo_table[ value ] = result
                return result
        return memoized
    else:
        return functools.partial( memoize, keyfn = keyfn )

def clocked( fun, output = sys.stderr ):
    """
    Decorator that clocks a function each time it is called.

    @param fun: function to clock
    @param output: output stream to use
    @returns: a wrapped function
    """
    @functools.wraps( fun )
    def call( *args, **kword ):
        """ 
        Call the function
        """
        # create and output message
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
        # handles a keyboard ^C in an interactive REPL
        print 'Interrupted'
        result = None
    end = time.time()
    # output message
    print >> sys.stderr, "Clocked %f" % (end-start)
    return result
