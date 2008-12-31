################################################################################
# File     : sysutil.py
# Function : System Utility Library
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

import time
import sys
import traceback
import functools 
from sequtil import first

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
        @functools.wraps( fun )
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



