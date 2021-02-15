## Class Motion

### Member Methods

**CONSTRUCTOR**
1. **`__init__`**   
This is a `constructor` that initializes the data members of the class.

**PUBLIC METHODS**  
1. **`move_object()`**  
This method is used to move the object, with whom, the motion is associated. Moving of an object is indepenednt of the object type, for free motion, this this method is apt to be in the `super class` instead of being redundantly in all sub-classes.

**PROTECTED METHODS**

1. **`_check_limit(x,y)`**  
This method is to check if the object will exceed the boundaries of the system, if it is displaced by x_d and y_d in the x and y axes respectively.

### Implementation of Inheritance

This motion class is `inherited` by moving entities of the game, like the Board/Plank and Ball classes.

## Class Ball

### Member Methods

**CONSTRUCTOR**

1. **`__init__`**   
This is a `constructor` that initializes the data members of the class.

**PUBLIC METHODS**

2. **`isDead()`**  
This method is called to see if the ball has died. As a rule, we consider the ball dead if it touches the (bottom wall - 5) vertical position, but given the mechanism of the game, the ball is dead when it misses the paddle, or goes beneath it.

3. **`reset(x,y)`**     
This method is used to reset the ball, to the middle of the paddle. The coordinates to set the ball at are given by (x,y)

4. **`move_object(plank)`**     
This method is used to move the ball. This is an example of `function overriding`, to change the property of the parent class `Motion` method `move_object`.

5. **`launch_object()`**    
This method is used to launch the ball to start the game, or in other related scenario. This is a `mutable function` as it changes the properties of the class variables.   

**PRIVATE METHODS**

It is trivial to understand that collision handling of a ball object is an intrinsic property of the object and no external component of the code needs to access this method, hence the private property.

1. **`__handle_wall_collision()`**  
This method handles the collision of the ball with the wall. It follows normal laws of reflections in this case.    



2. **`__handle_brick_collision()`**     
This handles the collision of the ball with the bricks. Note that, vertical, horizontial and oblique collisions are all taken into consideration.

3. **`__handle_plank_collision()`**     
This method handles the collision of ball with the plank. It takes care of the paddle grab powerUp if activated.

4. **`__check_collision()`**    
This method checks if collision has happened and returns the value of the collision type if it has happened. Return values contain :    
    1.  `"wall"` -> for collision with the wall
    2.  `"brick"` -> for collision with the brick
    3. `"plank"` -> for collision with the plank
    4. `"None"` -> if collision has not happened


### Implementation of Data Abstraction

Data abstraction is implemented as the user of the Ball class needs to only call `move_object()` function, and the functionalities of collisions with the brick, plank or wall is checked and handled by itself. 

