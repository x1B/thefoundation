var css = ( function()
{
   var SCALE_FACTOR = 10000;
   var SCALED_EM = SCALE_FACTOR + "em";
   
   function pixelsFromEm( emSize, contextNode )
   {
      var parent, node = $( "<div>" );
      if ( contextNode && contextNode.parentNode ) {
         parent = $( contextNode.parentNode ); 
      }
      else {
         parent = $( "body" );
      }
      parent.append( node.css( "width", SCALED_EM ) );
      var width = node.width() / SCALE_FACTOR * emSize;
      node.remove();
      return width;
   }
   
   return {
      pixelsFromEm: pixelsFromEm
   }
   
} )();
