################################################################################
# File     : utiltest.py
# Function : Utility Unit tests
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

import unittest
import strutil
import sequtil
import fnutil
import sysutil
import mathutil


class UtilTest( unittest.TestCase ):
    def setUp( self ):
        pass

    def test_chomp( self ):
        self.assertEqual( strutil.chomp( "hello world"), "hello world" )
        self.assertEqual( strutil.chomp( "hello world\r"), "hello world" )
        self.assertEqual( strutil.chomp( "hello world\r\n"), "hello world" )
        self.assertEqual( strutil.chomp( "hello world\n"), "hello world" )
        # takes off last \r but not the \n
        self.assertEqual( strutil.chomp( "hello world\n\r"), "hello world\n" )        
    def test_chomplines( self ):
        self.assertEqual( strutil.chomplines( ["hello", "goodbye"]), ["hello", "goodbye" ] )
        self.assertEqual( strutil.chomplines( ["hello\r", "goodbye\n"]), ["hello", "goodbye" ] )
        self.assertEqual( strutil.chomplines( ["hello\n", "goodbye\r"]), ["hello", "goodbye" ] )
        self.assertEqual( strutil.chomplines( ["hello\r\n", "goodbye"]), ["hello", "goodbye" ] )
    def test_istringcmp( self ):
        self.assertEqual( strutil.istringcmp( "hello", "HELLO" ), 0 )
        self.assertEqual( strutil.istringcmp( "hell", "HELLO" ), -1 )
        self.assertEqual( strutil.istringcmp( "hellO", "HELL" ), 1 )                
    def test_unzip( self ):
        a,b = ( [1,2,3], [4,5,6] )
        c = zip(a, b)
        self.assertEqual( sequtil.unzip( c ), ( a, b ) )
        a,b = ( [1,2,3,6], [4,5,6] )
        c = zip(a, b)
        self.assertEqual( sequtil.unzip( c ), ( a[:3], b ) )
        
    def test_count( self ):
        self.assertEqual( sequtil.count( [True, False] ), 1 )
        self.assertEqual( sequtil.count( ["", "Hello"] ), 1 )
        self.assertEqual( sequtil.count( [None, 1] ), 1 )
        self.assertEqual( sequtil.count( [0, 11] ), 1 )
        self.assertEqual( sequtil.count( [{},{'a':1}] ), 1 )
        self.assertEqual( sequtil.count( [1, 2, 3, 4, 'hello'] ), 5 )

    def test_countif( self ):
        self.assertEqual( sequtil.countif( mathutil.evenp, range( 1, 5 ) ), 2 )

    def test_mapinto( self ):
        a = range( 0, 4 )
        def fn ( x ):
            return x + 1
        b = map( fn, a )
        sequtil.mapinto( fn, a )
        self.assertEqual( a,  b )

    def test_partition( self ):
        a = range( 10 )
        evens = filter( mathutil.evenp, a )
        odds = filter( mathutil.oddp, a )
        ( truep, falsep ) = sequtil.partition( mathutil.evenp, a )
        self.assertEqual( truep, evens )
        self.assertEqual( falsep, odds ) 

        (truep, falsep ) = sequtil.partition( mathutil.evenp, evens )
        self.assertEqual( truep, evens )
        self.assertEqual( falsep, [] )

        (truep, falsep ) = sequtil.partition( mathutil.oddp, evens )
        self.assertEqual( truep, [] )
        self.assertEqual( falsep, evens )

        
    def test_removeif( self ):
        a = range( 10 )
        evens = filter( mathutil.evenp, a )
        odds = filter( mathutil.oddp, a )
        sequtil.removeif( mathutil.oddp, a )

        self.assertEqual( a, evens )

    def test_span( self ):
        a = range( 10 )

        result = ([2, 4, 6, 8], [1, 3, 5, 7])
        self.assertEqual( sequtil.span( mathutil.evenp, [2,4,6,8,1,3,5,7] ), result )
        
        self.assertEqual( sequtil.span( mathutil.oddp, a ), ( [],range( 10 ) ) )
        self.assertEqual( sequtil.span( lambda x: True, a ), ( range( 10 ), [] ) )

    def test_brk( self ):
        a = range( 10 )

        result = ([2, 4, 6, 8], [1, 3, 5, 7])
        self.assertEqual( sequtil.brk( mathutil.oddp, [2,4,6,8,1,3,5,7] ), result )
        
        self.assertEqual( sequtil.brk( mathutil.evenp, a ), ( [],range( 10 ) ) )
        self.assertEqual( sequtil.brk( lambda x: False, a ), ( range( 10 ), [] ) )

    def test_ipositions( self ):
        result = list( sequtil.ipositions( [1,None,False,0,'',4] ) )
        self.assertEqual( result, [0, 5]  )

        result = list( sequtil.ipositions( [None,False,0,''] ) )
        self.assertEqual( result, []  )

        result = list( sequtil.ipositions( range( 1, 10 ) ) )
        self.assertEqual( result, range( 9 )  )

    def test_iunique( self ):
        a = range( 5 ) + range( 5 )
        self.assertEqual( list( sequtil.iunique( a ) ), range( 5 ) )
        a = range( 5 ) 
        self.assertEqual( list( sequtil.iunique( a ) ), range( 5 ) )        

    def test_iterablep( self ):
        self.assertTrue( sequtil.iterablep( [] ) )
        self.assertTrue( sequtil.iterablep( {} ) )
        self.assertTrue( sequtil.iterablep( set() ) )
        self.assertFalse( sequtil.iterablep( 1 )  )
        self.assertFalse( sequtil.iterablep( None )  )
        self.assertTrue( sequtil.iterablep( mathutil.iprimes() )  )

    def test_iteratorp( self ):
        self.assertFalse( sequtil.iteratorp( [] ) )
        self.assertFalse( sequtil.iteratorp( {} ) )
        self.assertFalse( sequtil.iteratorp( set() ) )
        self.assertFalse( sequtil.iteratorp( 1 )  )
        self.assertFalse( sequtil.iteratorp( None )  )
        self.assertTrue( sequtil.iteratorp( mathutil.iprimes() )  )

    def test_first( self ):
        self.assertEqual( sequtil.first( [1] ), 1 )
        self.assertEqual( sequtil.first( [] ), None )

    def test_compose( self ):
        def f( x ):
            return x + 1
        def g( x ):
            return x * 2
        test1 = fnutil.compose( f, g )
        test2 = fnutil.compose( g, f )
        self.assertEqual( test1( 2 ), 5 )
        self.assertEqual( test2( 2 ), 6 )

    def test_identity( self ):
        self.assertEqual( fnutil.identity( None ), None )
        self.assertEqual( fnutil.identity( [1,2] ), [1,2] )        

    def test_memoize( self ):
        self.v = 0
        # function violates the permise of memoize therefore you can use
        # it to determine if cacheing is working
        @fnutil.memoize
        def incf( x ):
            self.v += 1
            return self.v
        def nonmemo_incf( x ):
            self.v += 1
            return self.v
        
        a = incf( 1 )
        b = incf( 2 )
        c = incf( 3 )
        self.assertEqual( incf( 1 ), a )
        self.assertEqual( incf( 2 ), b )
        self.assertEqual( incf( 3 ), c )
        self.assertNotEqual( nonmemo_incf( 1 ), a )
        self.assertNotEqual( nonmemo_incf( 2 ), b )
        self.assertNotEqual( nonmemo_incf( 3 ), c )                

        # incorrect keying function allows to test that keying is used
        # returns number of arguments so once called will always return
        # same value for each subsequent call of the same number of
        # arguments
        
        def keyfn( *x ):
            return len( *x )
        
        @fnutil.memoize( keyfn = keyfn )
        def test2( *x ):
            return list(x)

        test2( 3 )
        test2( 3,4 )        
        
        self.assertEqual( test2( 3 ), [3 ] )
        self.assertEqual( test2( 4 ), [3 ] )        
        self.assertEqual( test2( 3, 4 ), [ 3, 4 ] )
        self.assertEqual( test2( 1, 7 ), [ 3, 4 ] )                
        
        
if __name__ == "__main__":
    unittest.main()
