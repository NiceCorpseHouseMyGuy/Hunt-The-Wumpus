from Player import Player
from Wumpus import Wumpus
import time

# this has no reason to be here other than for fun.
helloworld = print

class Game:
    def __init__(self):
        self.Player = Player()
        self.Wumpus = Wumpus()

    def begin_game(self):
        helloworld("///////////////////////////////////////////////")
        helloworld()
        helloworld("The Blind Hunt")
        helloworld()
        helloworld("///////////////////////////////////////////////")
        self.prompt()

    def prompt(self):
        helloworld()
        helloworld("Your options are: (M)ove or (S)hoot")
        helloworld(f"You have {self.Player.arrows} Arrows left.")
        helloworld()
        action = input("What is your next action?: ")
        if action == "M" or action == "m":
            helloworld("I see you want to move.")
        elif action == "S" or action == "s":
            self.Player.shoot_arrow()
            helloworld("You shot me... you shot me pretty good.")
        else:
            helloworld("You can't do that.")
        helloworld()
        helloworld("///////////////////////////////////////////////")
        time.sleep(2)
        self.prompt()