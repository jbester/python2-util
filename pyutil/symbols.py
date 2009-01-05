class SymbolType(object):
    __slots__ = [ "name" ]
    def __setattr__( self, instance, value ):
        raise SyntaxError( "Cannot assign to a symbol" )
    def __init__( self, name ):
        super( SymbolType, self ).__setattr__( "name", name )
    def __eq__( self, param ):
        return isinstance( param, SymbolType ) and self.name == param.name
    def __repr__( self ):
        return 'SymbolType("%s")'%( self.name )
    def __str__( self ):
        return "<Symbol %s>"%( self.name )
         
class _Symbol( object ):
    def __getattr__( self, param ):
        return SymbolType( param )
    def get( self, param ):
        return SymbolType( param )
    def __setattr__( self, instance, value ):
        raise SyntaxError( "Cannot assign to a symbol" )

Symbol = _Symbol()

print 'ok'
