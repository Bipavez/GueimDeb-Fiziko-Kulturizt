This is a challenge designed for [/r/pygame](https://www.reddit.com/r/pygame/)  
[Link to challenge thread.](https://www.reddit.com/r/pygame/comments/3de4ng/challenge_drawing_in_the_right_order/)

This challenge should be pretty straight forward for those familiar with pygame.  It may take a little more effort for those who aren't, but I think it should be accessible to most.  If you participate I would be interested in whether or not you think it was way too easy, or way too hard (or just right for that matter).

**Challenge:**  
When creating a topdown rpg it is important that sprites are drawn in the correct order.  We want to avoid sprites overlapping like this:  
http://i.imgur.com/woOsQFA.png  
And instead make sure they look like this:  
http://i.imgur.com/nUeFu4G.png


When all the sprites can move independently, this means that the draw order is always changing.  The goal of this challenge is to make sure that sprites are always drawn in the correct order.


**Base code:**  
Running `main.py` will give you a screen with a number of NPCs running around and one user controlled character (with the arrow keys).   All of the sprites are members of a single sprite group (player included) called `App.all_Sprites`.  


**Suggestions:**  
In order to solve this challenge, you only need to edit the `main.py` file, though you are free to edit whatever you want.  
I suggest investigating different types of sprite groups:  
http://www.pygame.org/docs/ref/sprite.html  
The base problem can be solved by adding/editing about three lines of code if you know what you are aiming at.  If you want to go the extra mile, make your implementation use dirty sprites.  This will require changing the class from which `actors.RPGSprite` inherits, as well as possibly some other minor parts of the code in that file.


