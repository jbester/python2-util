################################################################################
# File     : strutil.py
# Function : String Library
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

import string
import re

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
