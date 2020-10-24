
# A Random Shooter Game

Name: Hongyi Chen (hongyic3)
Moderator: Nick Helms (nhelms2)

This is a random shooter game

#### Purpose
The purpose of this project is to create a game where a player can control a 

#### Motivation
There are plenty of games that involve the player controlling an entity that shoots bullets at an enemy until one or the other dies, but I’d like to create my own with my own features.

#### Technical Specification
 - Platform: PC (any PC that can run Python 3)
 - Programming languages: Python
 - Main libraries: PyGame
 - Stylistic conventions: PEP 8
 - IDE: PyCharm
 - Tools/Interfaces: Computer, external MongoDB database
 - Target audience: Anyone

#### Functionality

There should exist the following screens:
 - A main menu, where the player can choose to start a game, or go to the leaderboard. This is the screen that is seen when the application begins. 
 - A leaderboard screen, where the player can see the shortest time victories (based on entries from an external database). There should be a button to go back to the main menu.
 - A name entry screen, where the player can input their name if they win fast enough to get on the leaderboard. After submitting their name, the player should be redirected to the leaderboard screen.
 - A game screen, which allows the user to play a game. At the end, if the player wins and the time is a high score, the player should be redirected to the name entry screen. Otherwise, they should be returned to the main screen. More details below.

At the start of the game, the following should be displayed:
 - The player entity, with a circle around it
 - The enemy entity
 - A health bar for the player, at the bottom of the screen
 - A health bar for the enemy, at the top of the screen
 - A piece of text telling the player to put their cursor inside the circle surrounding the player entity, in order to begin the game

Once the player puts their cursor in the circle, the following should happen:
 - The player entity should follow the cursor, up to a maximum speed.
 - The player entity should shoot bullets towards the top of the screen
 - The enemy entity should shoot bullets according to one of several predefined attack patterns. After each attack pattern ends, a new randomly chosen one should begin next.
 - If an enemy bullet collides with the player entity, the player loses health and the bullet disappears. If a player bullet collides with the enemy entity, the enemy loses health and the bullet disappears. If the player entity collides with the enemy entity, both entities should lose health. 
 - If either entity reaches zero health, everything on the screen should be destroyed. Then, there should be a display saying either “You Win” or “You Lose”, depending on which entity was destroyed first. (The player is considered to win if both are destroyed at the same time.)
 - Pressing a certain key (perhaps X) will automatically kill the player.

#### Sketches
For sketches, see the sketches directory. 

#### Scope
This project aims to produce a functional game with a minimalistic but reasonably pleasing artistic design. It will NOT involve any fancy artwork. 


## Weekly requirements

#### Basic Timeline
 - Week 1: Implement a basic game screen, including all stages. Allow the user the control their character. The enemy will not be present.
 - Week 2: Implement the enemy, their bullets, and their attack patterns. At this point, the game screen should be fully functional.
 - Week 3: Implement all the other screens - main menu, leaderboard, and name input. The game should now be able to connect to the external database to retrieve and update leaderboard information. 

### Week 1


| Category | Total Score Allocated | Detailed Rubrics |
|-|:-:|-|
|  Game start stage |  4  |  0: Didn't implement anything <br> +2: Start stage includes all necessary elements for the week (player entity, starting circle, player health bar, instructions) <br> +1: Player entity does not do anything before the game begins <br> +1: Game can be begun by hovering cursor on the starting circle. |
|  Game over screen |  4  |  0: Didn't implement anything <br> +2: Game over screen includes all necessary text, and a button. <br> +2: Game over screen can be reached after the player dies |
|  Player Control During Game|  7  |  0: Didn't implement anything <br> +2: Player entity follows the cursor. <br> +1: Player entity has a fixed maximum movement speed. <br> +1: Player entity can be killed by pressing X (or another key) <br> +1: Dying should cause the screen to be wiped <br> +2: Bullets are implemented and player entity continuously shoots gray bullets upward after the game begins. |
|  Unit Testing |  6  |  0: No unit tests <br> +0.5 points per unit test |
|  Manual Testing |  4  |  0: No manual tests <br> +1 point for testing the start stage <br> +1 point for testing the user hovering their cursor to start the game <br> +1 point for testing player movement speed <br> +1 point for testing player death |

### Week 2
| Category | Total Score Allocated | Detailed Rubrics |
|-|:-:|-|
| Enemy at Start Stage | 4 | 0: Didn't implement anything <br> +2: Enemy is implemented, and is visible during the start stage <br> +1: Enemy has a visible health bar <br> +1: Enemy does not shoot before the game begins |
| You Win Screen | 2 | 0: Didn't implement anything <br> +1: If the enemy dies, the screen is wiped and the game is transitioned to the You Win screen <br> +1: The You Win screen displays time it took to win and a continue button. |
| Enemy Attack | 3 | 0: Didn't implement anything <br> +2: Once the game begins, the enemy begins spawning bullets to attack the player. <br> +1: The enemy can transition between different attack patterns |
| Attack Patterns | 6 | 0: Didn't implement anything <br> +2 per attack pattern, up to 3 attack patterns <br> -1 for each violation: At least 1 attack pattern should involve shooting directly towards the player. At least 1 attack pattern should involve bullets that can either split or spawn other bullets. At least 1 attack pattern should involve bullets that can change direction or speed after spawning |
| Unit Tests | 5 | 0: No unit tests <br> +.5 per unit test |
| Manual Tests | 5 | 0: No manual tests <br> 2 points: Some manual tests <br> 5 points: Thoroughly tests all possible events |



### Week 3
| Category | Total Score Allocated | Detailed Rubrics |
|-|:-:|-|
| Database connection | 3 | +1: Can connect to the database <br> +1: Can query the top scores in the database <br> +1: Can update the database <br> -1: Database key is committed to git |
| Main Menu | 2 | 0: Didn't implement anything <br> +1: There is a functioning button to start a game. <br> +1: There is a functioning button to view the leaderboard |
| Leaderboard | 3 | 0: Didn't implement anything <br> +2: The top 5 scores are displayed on the leaderboard. <br> +1: A button that redirects to the main menu |
| Name Input | 4 | 0: Didn't implement anything <br> +1: Allow the user to input a name <br> +1: Name should have a maximum length limit <br> +1: Allow the user to submit their high score, bringing them to the leaderboard page afterwards.<br> +1: Allow the user to cancel if they wish, effectively deleting their high score and bringing them to the main menu|
| Game End Transition | 3 | 0: Didn't implement anything <br> +1: The CONTINUE button on the game lose/win screen can redirect to the main menu <br> +2: If a high score was achieved, the button should instead redirect to the Name Input screen. |
| Unit tests | 2 | 0: No unit tests <br> +.5 per unit test |
| Manual Tests | 8 | 0: No manual tests <br> +2 for each screen tested (main menu, leaderboard, name input, game end) |