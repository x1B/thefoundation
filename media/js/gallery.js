var DURATION = 400;
var ViewMode = { GRID: { cssClass: "grid" }, ROW: { cssClass: "row" } };
var globals = { mode: null, editingEnabled: false }

$( document ).ready( function()
{
   $( "#set-row-view, #set-grid-view, #size-slider", $( "#tools" ) ).show();
   globals.mode =
      $( "#thumbs" ).hasClass( "grid" ) ? ViewMode.GRID : ViewMode.ROW;

   function disableSelection( element )
   {
      element.onselectstart = function() { return false; };
      element.unselectable = "on";
      element.style.MozUserSelect = "none";
   }

   disableSelection( $( "#thumbs" ).get( 0 ) );
   disableSelection( $( "#current" ).get( 0 ) );
   disableSelection( $( "#menu" ).get( 0 ) );

   var THUMB_WIDTH  = 164;
   var THUMB_HEIGHT = 110;
   var MIN_HEIGHT_PERCENT = 46;

   var thumbnailArea  = $( "#thumbs" );
   var thumbnailsList = $( "#thumbs .list" );
   var thumbLinks     = $( "a", thumbnailsList );
   var thumbnails     = $( "img", thumbnailsList );
   var imageArea      = $( "#current" );

   // [ viewMode,
   //   thumbMarginLeft, thumbMarginRight, thumbMarginBottom ,
   //   areaTop, areaWidth, areaHeight ]
   var rowValues = [ ViewMode.ROW,
                     thumbnails.css( "marginLeft" ),
                     thumbnails.css( "marginRight" ),
                     thumbnails.css( "marginBottom" ),
                     thumbnailArea.css( "top" ),
                     "132px" ];

   var gridValues = [ ViewMode.GRID, "10px", "10px", "0", "35px", "675px" ];

   function makeTransitionFunction( from, to )
   {
      return function( e )
      {
         if ( globals.mode == to[ 0 ] ) return;
         globals.mode = to[ 0 ];

         // Set start values for the animation.
         thumbnails.css( "marginLeft", from[ 1 ] ).
                    css( "marginRight", from[ 2 ] ).
                    css( "marginBottom", from[ 3 ] );
         thumbnailArea.css( "top", from[ 4 ] ).css( "height", from[ 5 ] );
         thumbnailArea.addClass( "transition" ).removeClass(
            from[ 0 ].cssClass
         );

         // Animate
         if ( to[ 0 ] == ViewMode.GRID ) {
            imageArea.slideUp( DURATION );
         }
         else {
            imageArea.slideDown( DURATION );
         }

         thumbnails.animate( { marginLeft: to[ 1 ],
                               marginRight: to[ 2 ],
                               marginBottom: to[ 3 ] }, DURATION );

         thumbnailArea.animate(
            { top: to[ 4 ], height: to[ 5 ] },
            DURATION,
            function()
            {
               thumbnailArea
                  .addClass( to[ 0 ].cssClass )
                  .removeClass( "transition" );
               if ( to[ 0 ] == ViewMode.GRID && globals.editingEnabled ) {
                  thumbnailsList.sortable( { smooth: false } );
               }
               else {
                  thumbnailsList.sortableDestroy();
               }
            }
         );
         $( "#tools" )
            .addClass( to[ 0 ].cssClass )
            .removeClass( from[ 0 ].cssClass );
      };
   }

   $( "#set-row-view" ).click( makeTransitionFunction( gridValues,
                                                       rowValues ) );
   $( "#set-grid-view" ).click( makeTransitionFunction( rowValues,
                                                        gridValues ) );

   var useTwoRows = false;

   $( "#size-slider" ).slider( {
      minValue: 0,
      maxValue: 100 - MIN_HEIGHT_PERCENT,
      startValue: 37,
      slide: function( e, ui )
      {
         var ratio = ( ui.slider.curValue + MIN_HEIGHT_PERCENT ) / 100;
         var height = Math.round( THUMB_HEIGHT * ratio );
         thumbnails.height( height );
         thumbLinks.width( Math.round( THUMB_WIDTH * ratio + 15 ) );

         if ( height <= 51 && !useTwoRows ) {
            var middleNode =
               thumbnails[ Math.round( thumbnails.length / 2 ) - 1 ];
            $( "<br>" ).insertAfter( middleNode.parentNode );
            useTwoRows = true;
         }
         else if( height > 51 && useTwoRows ) {
            $( ".list > br", thumbnailArea ).remove();
            useTwoRows = false;
         }
         thumbnailsList.toggleClass( "list-two-rows", useTwoRows )
      }
   } );

   function hideCurrent( e )
   {
      if ( globals.mode == ViewMode.GRID ) {
         $( "#current" ).removeClass( "grid" ).hide();
         $( "#cover" ).hide();
      }
   }

   $( "#cover" ).click( hideCurrent );
   $( "#current" ).click( hideCurrent );
   $( "#current img" ).click( function( e ) { e.preventDefault(); } );

   $( "#current" ).mouseover( function() { $( "#current #menu" ).show(); } );
   $( "#current" ).mouseout( function() { $( "#current #menu" ).hide(); } );


   var currentImageIndex = 0;

   function gotoImage( index )
   {
      if ( index == 0 ) {
         $( "#back-button" ).css( "visibility", "hidden" );
      }
      else if ( index + 1 == thumbLinks.size() ) {
         $( "#next-button" ).css( "visibility", "hidden" );
      }
      else {
         $( "#back-button, #next-button" ).css( "visibility", "visible" );
      }

      $( thumbLinks[ currentImageIndex ] ).removeClass( "current" );
      $( thumbLinks[ index ] ).addClass( "current" );

      var link = $( thumbLinks[ index ] );
      $( "a img", imageArea ).attr( "src", $( ".display-url", link ).text() );
      $( "#full-button a", imageArea ).attr( "href",
                                             $( ".full-url", link ).text() );

      if ( globals.editingEnabled ) {
         $( "#sidebar > h3 > input" ).attr( "value",
                                            $( "span", link ).text() );
         $.get( $( "img", link ).attr( "longdesc" ), { }, function( data )
         {
            $( "#sidebar > p > textarea" ).attr( "value", data );
         } );
      }
      else {
         $( "#sidebar > h3" ).empty().append( $( ".caption", link ).text() );
         $( "#sidebar > p" ).load( $( "img", link ).attr( "longdesc" ) );
      }

      currentImageIndex = index;
   }

   function makeStep( step )
   {
      return function( e )
      {
         e.stopPropagation();
         e.preventDefault();
         e.target.blur();
         gotoImage( currentImageIndex + step );

         if ( globals.mode != ViewMode.ROW ) return;

         var clipWidth = thumbnailArea.width();
         var link = $( thumbLinks[ currentImageIndex ] );
         var linkWidth = link.width();
         var offset = link[ 0 ].offsetLeft;
         var scrollLeft = thumbnailArea.scrollLeft();
         if ( offset < scrollLeft ) {
            // current thumbnail is to far to the left
            thumbnailArea.animate( { scrollLeft: offset - linkWidth }, 100 );
         }
         else if ( offset + linkWidth > scrollLeft + clipWidth ) {
            // current thumbnail is to far to the right
            thumbnailArea.animate(
               { scrollLeft: offset - clipWidth + linkWidth * 2 }, 100 );
         }
      };
   }

   $( "#back-button" ).click( makeStep( -1 ) );
   $( "#next-button" ).click( makeStep( 1 ) );

   $( "#thumbs a" ).click( function( e )
   {
      e.preventDefault();
      var link = e.target;
      if ( link.nodeName.toLowerCase() != "a" ) {
         link = e.target.parentNode;
      }
      gotoImage( thumbLinks.index( link ) );
      e.target.parentNode.blur();

      if ( globals.mode == ViewMode.GRID ) {
         imageArea.addClass( "grid" ).show();
         $( "#cover" ).fadeIn( 100 );
      }
      else {
         $( "#current" ).removeClass( "grid" ).show();
      }

   } );

   currentImageIndex = thumbLinks.index( $( "a.current" ).get( 0 ) );
   gotoImage( currentImageIndex );

   $( "#full-button" ).click( function()
   {
      location.href = $( "#current img" ).attr( "src" );
   } );

} );
