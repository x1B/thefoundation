/* This script is included only on management pages. */

// File upload re-styling script based on http://www.quirksmode.org/dom/inputfile.html
(function()
{
	if( !document.createElement || !document.getElementsByTagName ) return;
	
	var fakeFileInput = document.createElement( "div" );
	fakeFileInput.className = "fakefile";
	var fakeInput = document.createElement( "input" );
	fakeInput.readonly = "readonly";
	fakeInput.className = "text";
	fakeFileInput.appendChild( fakeInput );
	var fakeButton = document.createElement( "a" );
	fakeButton.setAttribute( "href", "javascript:void 0" );
	fakeButton.appendChild( document.createTextNode( " Select..." ) );
	fakeFileInput.appendChild( fakeButton );
	
	var inputsCollection = document.getElementsByTagName( "input" );		
	var input, inputs = [], i = 0;
	while ( input = inputsCollection[ i++ ] ) {
		if ( input.type == "file" ) inputs.push( input );
	}
	i = 0;
	while ( input = inputs[ i++ ] ) {
		input.className = "hidden file";
		var fakeClone = fakeFileInput.cloneNode( true );
		input.parentNode.insertBefore( fakeClone, input );
		// input.parentNode.appendChild( fakeClone );
		input.relatedElement = fakeClone.getElementsByTagName( "input" )[ 0 ];
		input.onchange = input.onmouseout = function () {
			this.relatedElement.value = this.value;
		}
	}
	
})();

/* Activate "upload new gallery" form */
activateFormLinks( $( "#new-gallery-form" ), $( "#show-new-gallery" ), $( "#cancel-new-gallery" ) );
