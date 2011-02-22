var colors = ( function()
{
   var HEX_SHORT = /#([0-9abcdefABCDEF])([0-9abcdefABCDEF])([0-9abcdefABCDEF])/;
   var HEX = /#([0-9abcdefABCDEF]{2})([0-9abcdefABCDEF]{2})([0-9abcdefABCDEF]{2})/;
   var RGB = /rgb\([ ]*(\d+),[ ]*(\d+),[ ]*(\d+)[ ]*\)/;
   
   return {
      R: 0,
      G: 1,
      B: 2,
      sum: function( a, b )
      {
         return [ a[0]+b[0], a[1]+b[1], a[2]+b[2] ];
      },
      
      delta: function( a, b )
      {
         return [ a[0]-b[0], a[1]-b[1], a[2]-b[2] ];
      },
      
      // scalar multiplication
      times: function( c, s )
      {
         return [ c[0] * s, c[1] * s, c[2] * s ];
      },
      
      parse: function( s )
      {
         var pattern, base;
         if ( s.charAt( 0 ) == "#" ) {
            pattern = ( s.length == 4 ) ? HEX_SHORT : HEX;
            base = 16;
         }
         else {
            pattern = RGB;
            base = 10;
         }
         var matches = s.match( pattern );
         if ( pattern == HEX_SHORT ) {
            matches[ 1 ] = matches[ 1 ] + matches[ 1 ];
            matches[ 2 ] = matches[ 2 ] + matches[ 2 ];
            matches[ 3 ] = matches[ 3 ] + matches[ 3 ];
         }
         return [ parseInt( matches[ 1 ], base ), 
                  parseInt( matches[ 2 ], base ), 
                  parseInt( matches[ 3 ], base ) ];
      },
      
      parseFloat: function( s )
      {
         return colors.times( colors.parse( s ), 1 / 255 );
      },
      
      asString: function( c )
      {
         return "rgb(" + parseInt( c[ 0 ] ) + "," + parseInt( c[ 1 ] ) + "," + parseInt( c[ 2 ] ) + ")";
      }
   };
   
} )();

