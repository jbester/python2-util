import unittest
import util


class UtilTest( unittest.TestCase ):
    def setUp( self ):
        pass

    def test_chomp( self ):
        self.assertEqual( util.chomp( "hello world"), "hello world" )
        self.assertEqual( util.chomp( "hello world\r"), "hello world" )
        self.assertEqual( util.chomp( "hello world\r\n"), "hello world" )
        self.assertEqual( util.chomp( "hello world\n"), "hello world" )
        # takes off last \r but not the \n
        self.assertEqual( util.chomp( "hello world\n\r"), "hello world\n" )        
    def test_chomplines( self ):
        self.assertEqual( util.chomplines( ["hello", "goodbye"]), ["hello", "goodbye" ] )
        self.assertEqual( util.chomplines( ["hello\r", "goodbye\n"]), ["hello", "goodbye" ] )
        self.assertEqual( util.chomplines( ["hello\n", "goodbye\r"]), ["hello", "goodbye" ] )
        self.assertEqual( util.chomplines( ["hello\r\n", "goodbye"]), ["hello", "goodbye" ] )
    def test_istringcmp( self ):
        self.assertEqual( util.istringcmp( "hello", "HELLO" ), 0 )
        self.assertEqual( util.istringcmp( "hell", "HELLO" ), -1 )
        self.assertEqual( util.istringcmp( "hellO", "HELL" ), 1 )                
    def test_unzip( self ):
        a,b = ( [1,2,3], [4,5,6] )
        c = zip(a, b)
        self.assertEqual( util.unzip( c ), ( a, b ) )
        a,b = ( [1,2,3,6], [4,5,6] )
        c = zip(a, b)
        self.assertEqual( util.unzip( c ), ( a[:3], b ) )
        
    def test_count( self ):
        self.assertEqual( util.count( [True, False] ), 1 )
        self.assertEqual( util.count( ["", "Hello"] ), 1 )
        self.assertEqual( util.count( [None, 1] ), 1 )
        self.assertEqual( util.count( [0, 11] ), 1 )
        self.assertEqual( util.count( [{},{'a':1}] ), 1 )
        self.assertEqual( util.count( [1, 2, 3, 4, 'hello'] ), 5 )

    def test_countif( self ):
        self.assertEqual( util.countif( util.evenp, range( 1, 5 ) ), 2 )

    def test_mapinto( self ):
        a = range( 0, 4 )
        def fn ( x ):
            return x + 1
        b = map( fn, a )
        util.mapinto( fn, a )
        self.assertEqual( a,  b )

    def test_partition( self ):
        a = range( 10 )
        evens = filter( util.evenp, a )
        odds = filter( util.oddp, a )
        ( truep, falsep ) = util.partition( util.evenp, a )
        self.assertEqual( truep, evens )
        self.assertEqual( falsep, odds ) 

        (truep, falsep ) = util.partition( util.evenp, evens )
        self.assertEqual( truep, evens )
        self.assertEqual( falsep, [] )

        (truep, falsep ) = util.partition( util.oddp, evens )
        self.assertEqual( truep, [] )
        self.assertEqual( falsep, evens )

        
    def test_removeif( self ):
        a = range( 10 )
        evens = filter( util.evenp, a )
        odds = filter( util.oddp, a )
        util.removeif( util.oddp, a )

        self.assertEqual( a, evens )

    def test_span( self ):
        a = range( 10 )

        result = ([2, 4, 6, 8], [1, 3, 5, 7])
        self.assertEqual( util.span( util.evenp, [2,4,6,8,1,3,5,7] ), result )
        
        self.assertEqual( util.span( util.oddp, a ), ( [],range( 10 ) ) )
        self.assertEqual( util.span( lambda x: True, a ), ( range( 10 ), [] ) )

    def test_brk( self ):
        a = range( 10 )

        result = ([2, 4, 6, 8], [1, 3, 5, 7])
        self.assertEqual( util.brk( util.oddp, [2,4,6,8,1,3,5,7] ), result )
        
        self.assertEqual( util.brk( util.evenp, a ), ( [],range( 10 ) ) )
        self.assertEqual( util.brk( lambda x: False, a ), ( range( 10 ), [] ) )

    def test_ipositions( self ):
        result = list( util.ipositions( [1,None,False,0,'',4] ) )
        self.assertEqual( result, [0, 5]  )

        result = list( util.ipositions( [None,False,0,''] ) )
        self.assertEqual( result, []  )

        result = list( util.ipositions( range( 1, 10 ) ) )
        self.assertEqual( result, range( 9 )  )

    def test_iunique( self ):
        a = range( 5 ) + range( 5 )
        self.assertEqual( list( util.iunique( a ) ), range( 5 ) )
        a = range( 5 ) 
        self.assertEqual( list( util.iunique( a ) ), range( 5 ) )        

    def test_iterablep( self ):
        self.assertTrue( util.iterablep( [] ) )
        self.assertTrue( util.iterablep( {} ) )
        self.assertTrue( util.iterablep( set() ) )
        self.assertFalse( util.iterablep( 1 )  )
        self.assertFalse( util.iterablep( None )  )
        self.assertTrue( util.iterablep( util.iprimes() )  )

    def test_iteratorp( self ):
        self.assertFalse( util.iteratorp( [] ) )
        self.assertFalse( util.iteratorp( {} ) )
        self.assertFalse( util.iteratorp( set() ) )
        self.assertFalse( util.iteratorp( 1 )  )
        self.assertFalse( util.iteratorp( None )  )
        self.assertTrue( util.iteratorp( util.iprimes() )  )

    def test_first( self ):
        self.assertEqual( util.first( [1] ), 1 )
        self.assertEqual( util.first( [] ), None )

    def test_compose( self ):
        def f( x ):
            return x + 1
        def g( x ):
            return x * 2
        test1 = util.compose( f, g )
        test2 = util.compose( g, f )
        self.assertEqual( test1( 2 ), 5 )
        self.assertEqual( test2( 2 ), 6 )

    def test_identity( self ):
        self.assertEqual( util.identity( None ), None )
        self.assertEqual( util.identity( [1,2] ), [1,2] )        

    def test_memoize( self ):
        self.v = 0
        # function violates the permise of memoize therefore you can use
        # it to determine if cacheing is working
        @util.memoize
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
        
        @util.memoize( keyfn = keyfn )
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
