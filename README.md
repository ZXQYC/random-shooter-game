# A Random Shooter Game

#### Final Project for CS 242 by Hongyi Chen

This is a simple shooter game made in Python 3, made using PyGame.

The game is now complete. Potential extensions in the future include:
 - Improving graphics
 - Adding different types of enemies
 - Adding more difficulty levels

## How to run

First, install Python 3 if you haven't already, and clone or download this repo.

Then, install requirements using this command:

    pip install -r requirements.txt

At the base directory, create a .env file and add the following line:

    ATLAS_KEY=YOUR ATLAS CONNECTION STRING HERE

Replace YOUR ATLAS CONNECTION STRING HERE with your atlas connection string, but
with the database name replaced with %s. For example:

    mongodb+srv://game:YOUR_PASSWORD_HERE@YOUR_CLUSTER_NAME_HERE.jmwxw.mongodb.net/%s?retryWrites=true&w=majority

Finally, run this command to play the game:

    python src
