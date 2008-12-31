################################################################################
# File     : signature.py
# Function : Type Signature Library
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
import string 
import decimal

_CHECK_SIGNATURES=True

def disable_signatures():
    "Disable checking of signatures"
    global _CHECK_SIGNATURES
    _CHECK_SIGNATURES = False

def _sig_enabled():
    global _CHECK_SIGNATURES
    return _CHECK_SIGNATURES

class SignatureType(object):
    def __init__( self ):
        object.__init__( self )
    def __str__( self ):
        return ""

class _AnyType(SignatureType):
    "Signature Type that accepts any type"
    def check( self, param ):
        return True
    def __str__( self ):
        return "<Any>"

class _NumericType(SignatureType):
    "Signature Type that accepts any numeric type"
    def check( self, param ):
        for typ in [int, long, float, decimal.Decimal]:
            if isinstance( param, typ ):
                return True
        return False
    def __str__( self ):
        return "<Numeric>"

class PolyType( SignatureType ):
    "Signature Type that accepts parameter that is any of the given types"
    def __init__( self, *typ ):
        self.typ = typ
    def check( self, param ):
        for t in self.typ:
            if deep_check( param, t ):
                return True
        return False
    def __str__( self ):
        if len( self.typ ) == 2:
            return "<%s>"%(string.join( map( str, self.typ ), ' or ' ))
        else:
            s = (string.join( map( str, self.typ[:-1] ), ', ' ))
            s += ", or %s"%(self.typ[-1])
            return "<%s>"%( s )

class OptionType(SignatureType):
    "Option Type accepts given type or None"
    def __init__( self, typ ):
        self.typ = typ
    def check( self, param ):
        # option type has type or is a none
        if param == None:
            return True
        return deep_check(  param, self.typ )
    def __str__( self ):
        return "<%s option>"%(self.typ)

class ListType(SignatureType):
    """List type accepts a list whose elements are of the same type provided 
Note: this different from just using the built in type list which acts as an
untyped list"""
    def __init__( self, typ ):
        self.typ = typ
    def check (self, param ):
        # make sure it's a list
        if not isinstance( param, list ):
            return False
        # don't check contents of list if it's an empty list
        if len( param ) == 0:
            return True
        # check contents of list
        else:
            return all( [deep_check( p, self.typ ) for p in param] )
    def __str__( self ):
        return "<%s list>"%(self.typ)

class TupleType(SignatureType):
    """Tuple Type accepts a tuple whose elemental types match the provided types
Note: this is different from just using the built in type tuple which acts
as an untyped tupel"""
    def __init__( self, *typ ):
        self.typ = typ
    def check( self, param ):
        if not isinstance( param, tuple ):
            return False
        # handle empty tuple
        if len( param ) == 0 and len( self.typ ) == 0:
            return True
        # check length of tuples to match
        elif len( param ) != len( self.typ ):
            return False
        # check each element against tuple types
        else:
            for (p,t) in zip( param, self.typ ):
                if not deep_check( p, t):
                    return False
            return True
    def __str__( self ):
        return "(%s)"%(string.join( map( str, self.typ ), ' * ' ))

# singleton instances of non parameteric types
AnyType = _AnyType()
NumericType = _NumericType()

def deep_check( param, typ ):
    "Perform a recursive check of types"
    # handle any type
    if isinstance( typ, SignatureType ):
        return typ.check( param )
    else:
        return isinstance( param, typ )

def signature( returnType, *argTypes ):
    "Signature decorator that checks return and parameter types"
    # error messages
    countMismatch = "Type count (%d) does not match argument count (%d)"
    argMismatch = "argument %r does not match expected type %s"
    retMismatch = "returned value %r does not match expected type %s"
    def signature_check( fn ):
        # check parameter count
        argc = len( argTypes )
        expected_argc = fn.func_code.co_argcount
        assert argc == expected_argc , countMismatch %(argc,expected_argc)
        
        @functools.wraps( fn )
        def func( *args, **kwds ):
            enabled = _sig_enabled()
            if enabled:
                # validate param types
                for (arg,typ) in zip (args, argTypes ):
                    assert deep_check( arg, typ ), argMismatch % ( arg, typ )    
            retVal = fn( *args, **kwds )
            # validate return type
            if enabled:
                assert deep_check(retVal,returnType),retMismatch % ( retVal, returnType )
            # return the result
            return retVal
        return func
    return signature_check

