var Deferred = ( function()
{
   function run( self, newState )
   {
      self.state_ = self.targetState_;
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
            this.targetState_ = null;
            callback();
            return;
         }
         else {
            var self = this;
            this.targetState_ = newState;
            this.timeout_ = setTimeout( function() { run( self ); },
                                        this.delayByState_[ newState ] );
         }
      }
      this.callbacks_.push( callback );
   }

   return Deferred;

} )();