/* thefoundation.de general effects, copyright (c)2008 Michael Kurze, 
 * depends on ./jquery.js, ./aninmation.js 
 */

var thefoundation = ( function()
{
   var MAIN = { }, GENERAL = { }, BLOG = { }
   var pageType = $( ".general_content" ).length ? GENERAL : ( $( "#people li.active" ).length ? BLOG : MAIN );
   
   var authors = [ "michael", "daniel", "david", "matthias" ];
   
   var columnHeightLimits = Animation.limits( labelMargin, $( "#people" ).height() - labelMargin, "px" );
   
   
   if ( pageType != BLOG ) {
      // Create author labels for the columns.
   	$( "body" ).append( $( "<h1>" ).attr( "id", "stat-caption" ) )
   	           .append( $( "<ul>" ).attr( "id", "stat-labels" ) );
	           
   	if ( pageType == GENERAL ) {
   	   $( "#stat-labels, #stat-caption" ).addClass( "general" );
      }
   	for ( var i = 0; i < authors.length; ++i ) {
   	   var name = authors[ i ].charAt( 0 ).toUpperCase() + authors[ i ].substring( 1 );
   	   $( "#stat-labels" ).append( $( "<li>" ).append( $( "<h2>" ).addClass( "name" ).text( name ) ) );
      }

      // These limits are global, so that they can be updated by the fix-method on window resize.
      var statLabelHeightLimits = Animation.limits( 0, 2.5, "em" );
      var labelMargin           = css.pixelsFromEm( statLabelHeightLimits.get().max );
      var topLimits             = Animation.limits( 0, $( "#people" ).height(), "px" );
   }

   // enable author based highlighting & tag based highlighting
   ( function()
   {
      if ( pageType == BLOG ) {
         return;
      }
      
      var ON = "ON", OFF = "OFF";
   
      // Create animations.   
      var linkColors = { "michael":  colors.parseFloat( "#dddf34" ), 
                         "daniel":   colors.parseFloat( "#b9df34" ), 
                         "david":    colors.parseFloat( "#dfa934" ), 
                         "matthias": colors.parseFloat( "#df5429" ) };                    
      var qs = $( "#core ul li a" );
      var linkColorDefault = colors.parseFloat( qs.css( "color" ) );
      var linkColorAnimations = { "michael": [], "daniel": [], "matthias": [], "david": [] };

      var statLabelsAnimation = Animation.create( Animation.cssProxy( $( "#stat-labels" ), 
                                                                      "height",
                                                                      statLabelHeightLimits ) );
      var columnHeightAnimations = { };
      var columnHeightLabels = { };
   
      // Tag based information: Create labels that display the article amount for the current tag per author.
      $( "#people > li" ).append( 
         $( "<div>" ).addClass( "statbar" ).append( $( "<div>" ).addClass( "label" ).append( "0" ) )
      );     
   
      for ( var i = authors.length; i --> 0; ) {
         var qs, author = authors[ i ];

         // author based highlighting - column/teaser opacity
         qs = $( "#people > li." + author );
      
         // author based highlighting - tag color
         $( "#core > ul > li" ).each( function( index, item )
         {
            var qs = $( item );
            var a = $( "a", $( item ) );
            var channelAnimations = Animation.forChannels( a, "color" );
            for ( var author in linkColorAnimations ) {
               if ( item.className.indexOf( "usage-" + author ) != -1 ) {
                  linkColorAnimations[ author ].push( channelAnimations );
               }
            }
         } );
      
         // tag based highlighting
         qs = $( "#people > li." + author + " > .statbar" );
         var heightProxy = Animation.cssProxy( qs, "height", columnHeightLimits );
         columnHeightAnimations[ author ] = Animation.create( heightProxy );
         columnHeightLabels[ author ] = $( ".label", qs );
      }
   
   
      // author based tag coloring //////////////////////////////////////////////////////////////////////////

      var hightime = new Deferred( { ON: 500, OFF: 200 } );

      $( "#teaser > li, #people > li" ).each( function( index, item )
      {
         $( item ).mouseover( function( e )
         {
            hightime.trigger( ON, function()
            {
               var author = $( item ).attr( "class" ).split( " " )[ 0 ];
               var linkColorAnimationsForAuthor;
               for ( var i = authors.length; i --> 0; ) {
                  if ( authors[ i ] == author ) continue;
                  linkColorAnimationsForAuthor = linkColorAnimations[ authors[ i ] ];
                  for( var j = linkColorAnimationsForAuthor.length; j --> 0; ) {
                     Animation.updateChannels( linkColorAnimationsForAuthor[ j ], linkColorDefault )
                  }
               }
            
               linkColorAnimationsForAuthor = linkColorAnimations[ author ];
               for( i = linkColorAnimationsForAuthor.length; i --> 0; ) {
                  Animation.updateChannels( linkColorAnimationsForAuthor[ i ], linkColors[ author ] )
               }
            
            } );
         } );
      } );
   
   
      $( "#core, #people, #teaser" ).each( function( index, item )
      {
         $( item ).mouseout( function( e )
         {
            if( $( item ).get( 0 ) != e.relatedTarget ) {
               hightime.trigger( OFF, function()
               {
                  for ( var i = authors.length; i --> 0; ) {
                     var linkColorAnimationsForAuthor = linkColorAnimations[ authors[ i ] ];
                     for( var j = linkColorAnimationsForAuthor.length; j --> 0; ) {
                        Animation.updateChannels( linkColorAnimationsForAuthor[ j ], linkColorDefault )
                     }
                  }
               
               } );
            }
         } );
      } );


      // tag based: stat bars ///////////////////////////////////////////////////////////////////////////////

      var tooltime = new Deferred( { ON: 700, OFF: 200 } );
      var STAT_EXP = /usage-([a-zA-Z]+)-([0-9]+)/g;

      $( "#topics > li, #archive > li" ).each( function( index, element )
      {
         var noStatsTimeout;
         $( element ).mouseover( function( e )
         {
            tooltime.trigger( ON, function()
            {
               clearTimeout( noStatsTimeout );
               $( "#people" ).addClass( "stats" );

               // Display labels at the bottom of the columns.
               statLabelsAnimation.setTarget( 1 );
            
               // parse the individual amounts of articles
               var match, className = $( element ).attr( "class" );
               var amounts = { }, sum = 0, max = 0.1;
               for ( var i = authors.length; i --> 0; ) amounts[ authors[ i ] ] = 0;
               while ( match = STAT_EXP.exec( className ) ) {
                  var amount = parseInt( match[ 2 ] );
                  sum += amounts[ match[ 1 ] ] = amount;
                  max = Math.max( max, amount );
               }
               
               $( "#stat-caption" ).text( "articles in " + $( element ).text() );

               // display them using the statbar mask
               for ( var author in amounts ) {
                  // We need some space at the bottom, for the column labels (the author names).
                  var ratio = amounts[ author ] / max;
                  var target = 1 - ratio;
                  columnHeightLabels[ author ].text( amounts[ author ] );
                  columnHeightAnimations[ author ].setTarget( target );
               }
            
            } );
         } );
      
      
         $( element ).mouseout( function( e )
         {
            tooltime.trigger( OFF, function()
            {
               $( "#stat-caption" ).text( "" );

               statLabelsAnimation.setTarget( 0 );
               for ( var i = 0; i < authors.length; ++i ) {
                  columnHeightAnimations[ authors[ i ] ].setTarget( 0 );
               }
               noStatsTimeout = setTimeout( function() { $( "#people" ).removeClass( "stats" ) }, 550 );
            } );
         } );
      
      } );
   
   } )();

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   /**
    * The amount of vertical space which is available to display the gallery browser.
    */
   function availableSpace()
   {
       return { height: window.innerHeight || document.documentElement.clientHeight,
                width: window.innerWidth || document.documentElement.clientWidth };
   }

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   /**
    * Adapt gallery browser size for small screens.
    */
   function fixGalleryBrowserSize()
   {
      var space = availableSpace();
      var browser = $( "#gallery-browser" );
      var closeButton = $( "#gallery-canvas span" );
      
      if ( space.height < browser.height() || space.width < browser.width() ) {
         browser.height( space.height ).
                 width( space.width ).
                 css( "left", $( "html" ).get( 0 ).scrollLeft ).
                 css( "top", $( "html" ).get( 0 ).scrollTop ).
                 css( "margin-left", 0 ).
                 css( "margin-top", 0 );
         closeButton.
                 css( "margin-left", "0" ).
                 css( "margin-top", "0" ).
                 css( "left", "986px" ).
                 css( "top", "2px" );
      }
      else {
         browser.height( "" ).
                 width( "" ).
                 css( "left", "" ).
                 css( "top", "" ).
                 css( "margin-left", "" ).
                 css( "margin-top", "" );
         closeButton.
                 css( "margin-left", "" ).
                 css( "margin-top", "" ).
                 css( "left", "" ).
                 css( "top", "" );
      }
   }

   /* maintain the height of 100% for the blogs */
   (function() 
   {
      var space = availableSpace();
      var peoplePadding = parseInt( $( "#people li" ).css( "padding-top" ) );

      function fix()
      {
         $( "#people > li" ).css( "height", "auto" );
         var ownHeight = $( "#people" ).height();
      
         var heights = [ ownHeight, $( "#core" ).height() ]
         var generalContent = $( ".general_content" );
         var teasers = $( "#teaser" );
         if ( teasers && teasers.height() > 0 ) {
            heights.push( teasers.height() + teasers.offset().top + 1 );
         }
         if ( generalContent.height() > 0 ) {
            heights.push( generalContent.height() + generalContent.offset().top + 1 );
         }
         if ( space.height > ownHeight ) {
            heights.push( space.height );
         }
         
         var height = Math.max.apply( Math, heights );
         var scrollTop = $( "html" ).get( 0 ).scrollTop;
         $( "#people > li" ).css( "height", height - peoplePadding );
         columnHeightLimits.set( { min: labelMargin + scrollTop,
                                   max: space.height + scrollTop, 
                                   unit: "px" } )
         $( "#stat-labels" ).css( "bottom", parseInt( -scrollTop ) + "px" );
         
         fixGalleryBrowserSize();
      }
   
      $( document ).ready( fix );
      $( window ).resize( fix );
      $( document ).scroll( fix );
      $( window ).load( fix );      

   } )();

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   // funkytize it, baiiitch!
   (function()
   {
      var FUNKY_NUMBER = 4;
   
      var element = $( ".general_content h1" );
      if ( $( ".general_content" ).attr( "id" ) == "error" ) {
         return;
      }
      var text = element.text();   
      var funk = "";
      for ( var i = 0; i < text.length; ++i ) {
         funk += '<span class="c-' + ( (i+1) % FUNKY_NUMBER + 1 ) + '">' + text.charAt( i ) + '</span>';
      }
   
      element.html( funk );
   
   } )();

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   /**
    * Allow to fade a form in/out if javascript is enabled.
    *
    * @param form:jQuery
    * @param showLinks:jQuery -- link(s) to a page that show our form
    * @param hideLinks:jQuery -- link(s) to sensible return-pages
    */
   function activateFormLinks( form, showLinks, hideLinks )
   {
      showLinks.click( function( e )
      {
         form.fadeIn( "fast" );
         $( "input", form ).get( 0 ).focus();
         e.preventDefault();
      } );
   
      hideLinks.click( function( e )
      {
         form.fadeOut( 'fast' );
         form.children( ".messages" ).html( "&nbsp;" );
         e.preventDefault();
      } );
   }

   activateFormLinks( $( "#login-form" ), $( "#show-login" ), $( "#cancel-login" ) );

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   /**
    * Enable JS based gallery display.
    */
   (function()
   {   
      /* helper */   
      scrollY = function()
      {
         if ( document.documentElement && document.documentElement.scrollTop )
            return document.documentElement.scrollTop;
         if ( document.body && document.body.scrollTop ) 
            return document.body.scrollTop;
         if ( window.pageYOffset ) 
            return window.pageYOffset;
         if ( window.scrollY ) 
            return window.scrollY;
      }
      
      var links = $( "a[href^='/gallery/']" );
      if ( !links.length ) return;
      
      function moveLabel( event )
      {
         var offset = $( "#gallery-browser" ).offset();
         var left = event.clientX - offset.left + 6, right = event.clientY - offset.top + 3;
         $( "label", closeButton ).css( "left", left ).css( "top", right );
      }
      
      var closeButton = $( "<span>" ).attr( "id", "close-gallery" ).html( "&nbsp;" )
                        .append( $( "<label>" ).html( "close&nbsp;gallery" ) )
                        .mousemove( moveLabel )
                        .mouseover( moveLabel )
      
      var canvas = $( "<div>" ).attr( "id", "gallery-canvas" ).
         append( $( "<div>" ).attr( "id", "gallery-background" ) ).
         append( $( "<iframe>" ).attr( "id", "gallery-browser" ) ).
         append( closeButton );

      $( "body" ).append( canvas );

      links.click( function( event )
      {
            
         $( "html" ).css( "overflow", "hidden" );
         $( "#gallery-canvas" ).css( "top", scrollY() );
         $( "#gallery-browser" ).css( "top", scrollY() );
         canvas.fadeIn( 300, function() {
            var galleryUrl = ( event.currentTarget || event.target ).href;
            if ( $( "#gallery-browser" ).attr( "src" ) == galleryUrl ) return; 
            $( "#gallery-browser" ).attr( "src", galleryUrl );
            fixGalleryBrowserSize();
         } );
         return false;
      } );

      $( "#gallery-background, #gallery-canvas > span" ).click( function()
      {
         canvas.fadeOut( 300, function() { $( "html" ).css( "overflow", "" ) } );
      } );
      
   })();

   //////////////////////////////////////////////////////////////////////////////////////////////////////////

   return { };
   
} )();