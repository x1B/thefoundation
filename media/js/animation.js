/**
 * Animate (CSS) properties to target values that can be changed at any time,
 * using a totally unrealistic model of acceleration and deceleration.
 */
var Animation = ( function()
{
   /**
    * A value holder that notifies all observers of value changes.
    * @param Object optionalValue An initial set of properties.
    */
   function ValueHolder( optionalValue )
   {
      this.v_ = optionalValue != null ? optionalValue : null;
      this.o_ = [ ];
      this.m_ = [ ];
   }

   /** Add an observer for value changes.
    *
    * @param Object observer The context object that needs to observe.
    * @param Function method The callback for update notification.
    */
   ValueHolder.prototype.addObserver = function( observer, method )
   {
      this.o_.push( observer );
      this.m_.push( method );
   }

   ValueHolder.prototype.removeObserver = function( observer )
   {
      var i = this.o_.indexOf( observer );
      this.o_.splice( i, 0 );
      this.m_.splice( i, 0 );
   }

   /** Modify the stored value, notifying observers.
    *
    * @param Object value The new value.
    * @param Object optionalOrigin The object that triggered the change,
    *                              it won't be notified.
    */
   ValueHolder.prototype.set = function( value, optionalOrigin )
   {
      if ( this.v_ == value ) return false;
      this.v_ = value;
      for ( var i = this.o_.length; i --> 0; ) {
         if ( this.o_[ i ] != optionalOrigin ) {
            this.m_[ i ].call( this.o_[ i ], value );
         }
      }
   }

   /**
    * @return Object The current value.
    */
   ValueHolder.prototype.get = function()
   {
      return this.v_;
   }


   /**
    * Encapsulate a css property of a html element and allow to access it as
    * a value between zero and one.
    *
    * The value of zero is mapped to the lower limit, the value of one to the
    * upper limit. Observers can register, to be notified when values change.
    *
    * Implement your own range proxy to control other things such as
    * percentages, colors or even non-css values such es html text-data.
    * Simply extend and override the methods {@link #updateView} and
    * {@link #updateValue}.
    *
    * @param QuerySet querySet A jQuery set to control.
    * @param String propertyName The css property to control.
    * @param ValueHolder limits A source of min/max value, to which zero and
    *                           one are mapped.
    */
   function CssRangeProxy( querySet, propertyName, limits )
   {
      // inheritance
      if ( arguments.length == 0 ) return;

      this.qs_ = querySet;
      this.p_ = propertyName;
      limits.addObserver( this, this.updateLimits );
      this.updateLimits( limits.get() );
      ValueHolder.call( this, this.v_ );
   }

   CssRangeProxy.prototype = new ValueHolder;

   CssRangeProxy.prototype.set = function( value, optionalOrigin )
   {
      this.updateView( value );
      ValueHolder.prototype.set.call( this, value, optionalOrigin || null );
   }

   CssRangeProxy.prototype.updateLimits = function( limits )
   {
      this.min_ = limits.min;
      this.delta_ = limits.max - limits.min;
      this.unit_ = limits.unit;
      this.updateValue();
   }

   /**
    * Read the value from the current DOM state, used for initialization.
    * @protected
    */
   CssRangeProxy.prototype.updateValue = function()
   {
      this.v_ = ( parseFloat( this.qs_.css( this.p_ ) )
                  - this.min_ ) / this.delta_;
   }

   /**
    * Update the DOM state to the current value, this is used during
    * animation.
    * @protected
    */
   CssRangeProxy.prototype.updateView = function( value )
   {
      this.qs_.css( this.p_, this.min_ + value * this.delta_ + this.unit_ );
   }


   /**
    * Proxy to animate between colors.
    */
   function ColorRangeProxy( querySet, propertyName, limits )
   {
      CssRangeProxy.call( this, querySet, propertyName, limits );
   }

   ColorRangeProxy.prototype = new CssRangeProxy();

   ColorRangeProxy.prototype.updateLimits = function( limits )
   {
      this.min_ = colors.parse( limits.min );
      this.delta_ = colors.delta( colors.parse( limits.max ), this.min_ );
      this.updateValue();
   }

   // To avoid conflicts, the value is simply updated using the first channel
   // that has non-zero delta.
   ColorRangeProxy.prototype.updateValue = function()
   {
      // Choose channel to compare.
      for ( var i = 3; i --> 0; ) if ( this.delta_[ i ] != 0 ) break;
      // Update value using selected channel.
      this.v_ = ( colors.parse( this.qs_.css( this.p_ ) )[ i ]
                  - this.min_[ i ] ) / this.delta_[ i ];
   }

   ColorRangeProxy.prototype.updateView = function( value )
   {
      var c = colors.sum( this.min_, colors.times( this.delta_, value ) );
      this.qs_.css( this.p_, colors.asString( c ) );
   }

   /**
    * Proxy to animate individual channels of css color properties
    * independently.
    *
    * @param String channel colors.R colors.G, colors.B
    */
   function ChannelRangeProxy( querySet, propertyName, channel, limits )
   {
      this.channel_ = channel;
      CssRangeProxy.call( this, querySet, propertyName, limits );
   }

   ChannelRangeProxy.prototype = new CssRangeProxy();

   ChannelRangeProxy.prototype.updateValue = function()
   {
      // Update value using selected channel.
      this.v_ = ( colors.parse( this.qs_.css( this.p_ ) )[ this.channel_ ]
                  - this.min_ ) / this.delta_;
   }

   ChannelRangeProxy.prototype.updateView = function( value )
   {
      var c = colors.parse( this.qs_.css( this.p_ ) );
      c[ this.channel_ ] = this.min_ + value * this.delta_;
      this.qs_.css( this.p_, colors.asString( c ) );
   }


   function Animation( propertyProxy, length )
   {
      this.time_ = length;
      this.timeslice_ = DELAY / this.time_;
      this.proxy_ = propertyProxy;
      propertyProxy.addObserver( this, this.updateDistance );

      this.velocity_ = 0;
      this.done_ = true;

      animations.push( this );
      this.setTarget( propertyProxy.get() );
   }

   /**
    * Create an animation to control one css-property of an html element.
    * The animation is always performed from current value to the current
    * target value. Thus the only way to control the animation itself is to
    * control the target value.
    *
    * Both of these values may be changed at any time from the outside.
    *
    * @param CssRangeProxy proxy A range proxy to be controlled by the
    *                      animation. The proxy also provides the initial
    *                      value for the animation.
    * @param Function optionalCallback A method to call when the animation
    *                                  has finished.
    *
    * @return ValueHolder Contains the current value between 0 and 1.
    *                     Call set( ... ) to start the animation to the
    *                     new target value.
    */
   Animation.create = function( proxy, length )
   {
      return new Animation( proxy, length || Length.NORMAL );
   }

   /**
    * Shortcut for very simple pixel-size animations.
    */
   Animation.forPixelRange = function( querySet, propertyName, optionalFrom,
                                       optionalTo )
   {
      return Animation.create(
          new CssRangeProxy( querySet, propertyName,
                             Animation.limits( optionalFrom || 0,
                                               optionalTo || 0, "px" ) )
      );
   }

   /**
    * @return ValueHolder A new observable proxy with the given values for
    *                     the "min" and "max" properties.
    */
   Animation.limits = function( min, max, unit )
   {
      return new ValueHolder( { min: min, max: max, unit: unit } );
   }

   var R = colors.R, G = colors.G, B = colors.B;

   /**
    * Create three animations, one for each channel of the given color
    * property.
    *
    * The resulting three targets are returned in an array.
    */
   Animation.forChannels= function( querySet, propertyName )
   {
      var red = Animation.channelProxy( querySet, propertyName, R );
      var green = Animation.channelProxy( querySet, propertyName, G );
      var blue = Animation.channelProxy( querySet, propertyName, B );
      return [ Animation.create( red, Length.SHORT ),
               Animation.create( green, Length.SHORT ),
               Animation.create( blue, Length.SHORT ) ];
   }

   Animation.updateChannels = function( animations, color )
   {
      animations[ R ].setTarget( color[ R ] );
      animations[ G ].setTarget( color[ G ] );
      animations[ B ].setTarget( color[ B ] );
   }

   /**
    * @param QuerySet querySet The jQuery set to animate.
    * @param String propertyName The property to animate on the given set.
    *                            A rangeProxy is created, to convert between
    *                            css values and the [0...1] range used by the
    *                            animation.
    * @param ValueHolder optionalLimits Updateable min/max values for range
    *                                   conversion.
    */
   Animation.cssProxy = function( querySet, propertyName, optionalLimits )
   {
      return new CssRangeProxy(
         querySet,
         propertyName,
         optionalLimits || Animation.limits( 0, 1, "" )
      );
   }

   /**
    * Animates a css color value so that all channels reach the target at the
    * same time.
    */
   Animation.colorProxy = function( querySet, propertyName, optionalLimits )
   {
      return new ColorRangeProxy(
          querySet,
          propertyName,
          optionalLimits || Animation.limits( "#000000", "#ffffff", "" )
      );
   }

   /**
    * Animates one channel of a color.
    * @param String channel One of colors.R, colors.G and colors.B
    */
   Animation.channelProxy = function( querySet,
                                      propertyName,
                                      channel,
                                      optionalLimits )
   {
      return new ChannelRangeProxy(
         querySet,
         propertyName,
         channel,
         optionalLimits || Animation.limits( 0, 255, "" )
      );
   }

   Animation.prototype.setTarget = function( targetValue )
   {
      this.target_ = targetValue;
      this.updateDistance();
   }

   Animation.prototype.target = function()
   {
      return this.target_;
   }

   var abs = Math.abs, max = Math.max, min = Math.min;

   var THRESHOLD = 0.001;
   var ACCELERATION = 8;
   var BRAKE_ACCELERATION = 5;
   var BRAKE_ACCELERATION_MAX = 27;
   var VELOCITY_MAX = 3;

   /**
    * @return Boolean <tt>false</tt> if this animation has more steps,
    *                 <tt>true</tt> if it is done.
    */
   function step( self )
   {
      if ( self.done_ ) {
         return true;
      }

      // Calculate the acceleration, which depends on the velocity and on the
      // remaining distance to the target.
      // - If the velocity is not in the target direction, use maximum
      //   deceleration.
      // - Else, if the velocity has to be reduced to reach zero before the
      //   target is hit, use the lowest possible (absolute) acceleration in
      //   range [ BRAKE_ACCELERATION ... BRAKE_ACCELERATION_MAX ].
      // - Else, if the max velocity has reached VELOCITY_MAX, zero
      //   acceleration is used.
      // - Else, the velocity is increased, using ACCELERATION.

      var a, v = self.velocity_, d = self.distance_,
             timeslice = self.timeslice_;

      // The signum of velocity and distance is important for the direction
      // of the acceleration.
      var sgnV = v < 0 ? -1 : 1;
      var sgnD = d < 0 ? -1 : 1;

      // Stop/Brake-Acceleration; use it to reach a velocity of zero at the
      // target.
      // NEEDS FIX B: The last factor should be 1, accordings to mechanics.
      // But 0.7 works better - why?
      var stopAcceleration = ( 0.5 * ( -abs(v) / d ) + ( -(v*v) / d ) ) * 0.7
      var sgnSA = stopAcceleration < 0 ? -1 : 1;
      // The absolute value of the stop acceleration - for comparisions to
      // the brake acceleration.
      var absoluteStopAcceleration = abs( stopAcceleration );

      // Do we need to turn around?
      if ( sgnV != sgnD && v != 0 ) {
         a = (-sgnV) * min( BRAKE_ACCELERATION_MAX, ( sgnV * v )/timeslice );
      }
      else if ( abs( d ) < 0.5
                && absoluteStopAcceleration > BRAKE_ACCELERATION ) {
         a = min( absoluteStopAcceleration, BRAKE_ACCELERATION_MAX ) * sgnSA;
      }
      // Are we at max speed?
      else if ( v * sgnV == VELOCITY_MAX ) {
         a = 0;
      }
      // Can we reach max speed now?
      else if ( sgnV * v + ACCELERATION * timeslice > VELOCITY_MAX ) {
         a = ( sgnV * VELOCITY_MAX - v ) / timeslice;
      }
      else {
         a = sgnD * ACCELERATION;
      }

      if ( abs( d ) < 2 * abs( v ) * timeslice ) {
         self.velocity_ = self.distance_ = 0;
         self.proxy_.set( self.target_, self );
         self.done_ = true;
         return true;
      }

      self.velocity_ = v + a * timeslice;
      self.distance_ -= (self.velocity_+v) * 0.5 * timeslice;
      self.distance_ -= self.velocity_ * timeslice;
      self.proxy_.set( self.target_ - self.distance_, self );

      return false;
   }

   Animation.prototype.updateDistance = function()
   {
      this.distance_ = this.target_ - this.proxy_.get();
      if ( Math.abs( this.distance_ ) > 0 ) {
         this.done_ = false;
         if ( interval == null ) run();
      }
   }

   // Measure of...
   // ...time is milliseconds.
   // ...distance is the "unit" (from 0 to 1).
   // ...velocity is "units per animation-duration".
   // ...acceleration is "units per animation-duration" / animation-duration.
   var DELAY = 20;

   // Provide named choices for animation length.
   var Length = Animation.Length = {
      LONG: 1440,
      NORMAL: 1000,
      SHORT: 360
   };

   var interval = null;
   var animations = [ ];

   function run()
   {
      var stop = true;
      for ( var i = animations.length; i --> 0; ) {
         stop = step( animations[ i ] ) && stop;
      }
      if ( stop ) {
         window.clearInterval( interval );
         interval = null;
      }
      else if ( interval == null ) {
         interval = setInterval( run, DELAY );
      }
   }

   function f( a )
   {
      var s = "";
      if ( a >= 0 ) s += " ";
      if ( abs( a ) < 10 ) s += " ";
      return s + a.toFixed( 5 );
   }

   /**
    * @param Number d The remaining distance to the target, usually (but not
    *                 necessarily) from [-1 ... 1].
    * @param Number v The current velocity, from [ -VELOCITY_MAX ...
    *                 VELOCITY_MAX ].
    * @param Number timeslice The unit-fraction used to generate velocities
    *                         and acceleration values.
    *
    * @return Number The acceleration to use.
    */
   function acceleration( d, v, timeslice )
   {
      return a;
   }

   return Animation;

} )();
