var Deferred = ( function()
{
   function run( self, newState )
   {
      self.state_ = self.targetState_;
      // console.log( "updated state to %o", self.state_ );
      self.targetState_ = null;
      for ( var i = self.callbacks_.length; i --> 0; ) {
         self.callbacks_[ i ]();
      }
   }
   
   function Deferred( delayByState )
   {
      this.delayByState_ = delayByState;
      this.timeout_ = null;
      this.state_ = null;
      this.targetState_ = null;
      this.callbacks_ = [ ];      
   }
   
   Deferred.prototype.trigger = function( newState, callback )
   {
      if ( newState == this.state_ || newState != this.targetState_ ) {
         clearTimeout( this.timeout_ );
         this.callbacks_ = [ ];
         
         if ( newState == this.state_ ) {
            // console.log( "newState (%o) == .state_ (%o)", newState, this.state_  );
            this.targetState_ = null;
            callback();
            return;
         }
         else {
            // console.log( "newState (%o) != .targetState_ (%o)", newState, this.targetState_ );
            var self = this;
            this.targetState_ = newState;
            this.timeout_ = setTimeout( function() { run( self ); }, this.delayByState_[ newState ] );
         }
      }
      //else {
      //  console.log( "newState (%o) == .targetState_ (%o)", newState, this.targetState_ );
      //}
      // We are already on our way to this target state, just add the callback.
      this.callbacks_.push( callback );
   }
   
   return Deferred;
   
} )();