$( "document" ).ready( function()
{
   /////////////////////////////////////////////////////////////////////////////////////////////////////

   var galleryTitle = $( "#tools h2" )[ 0 ];
   var imageTitle = $( "#sidebar > h3" )[ 0 ];
   var longDescription = $( "#sidebar > p" )[ 0 ];

   function toggleEditing()
   {
      if ( globals.editingEnabled ) { disableEditing(); } else { enableEditing(); };
   }

   function enableEditing()
   {
      if ( globals.editingEnabled ) return;
      globals.editingEnabled= true;
   
      $( "#edit-button" ).addClass( "selectedTool" );
      if ( globals.mode == ViewMode.GRID ) {
         $( "#thumbs .list" ).sortable( { smooth: false } );
      }
      
      galleryTitle.innerHTML = 
         '<input class="editing" name="edit-gallery-title" value="' + galleryTitle.innerHTML + '" />';
      imageTitle.innerHTML =
         '<input class="editing" name="edit-gallery-title" value="' + imageTitle.innerHTML + '" />';
      longDescription.innerHTML = '<textarea class="editing">' + longDescription.innerHTML + "</textarea>";
   }
      
   function disableEditing()
   {
      if ( !globals.editingEnabled ) return;
      globals.editingEnabled = false;
         
      galleryTitle.innerHTML = galleryTitle.firstChild.value;
      imageTitle.innerHTML = imageTitle.firstChild.value;
      longDescription.innerHTML = longDescription.firstChild.value;
      
      $( "#edit-button" ).removeClass( "selectedTool" );
      $( "#thumbs .list" ).sortableDestroy();
   }
   
   $( "#edit-button" ).click( toggleEditing );

   /////////////////////////////////////////////////////////////////////////////////////////////////////
   
} );
