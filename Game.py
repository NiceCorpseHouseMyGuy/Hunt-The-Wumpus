from Player import Player
from Wumpus import Wumpus
import time
import pygame

# this has no reason to be here other than for fun.
helloworld = print

# sounds aren't really necessary but fun.

pygame.init()
pygame.mixer.init()

sfx_select = pygame.mixer.Sound('sounds/select.ogg')

class Game:
    def __init__(self):
        self.Player = Player()
        self.Wumpus = Wumpus()
        self.memory = None

    def begin_game(self):
        helloworld("===============================================")
        helloworld("                The Blind Hunt                 ")
        helloworld("===============================================")
        self.introduction()

    def prompt(self):
        helloworld("Your options are: (M)ove or (S)hoot or (Q)uit.")
        helloworld(f"You have {self.Player.arrows} Arrows left.")
        helloworld()
        action = input("What is your next action?: ")
        pygame.mixer.Sound.play(sfx_select)
        if action == "M" or action == "m":
            helloworld("I see you want to move.")
        elif action == "S" or action == "s":
            self.Player.shoot_arrow()
            helloworld("You shot me... you shot me pretty good.")
        elif action == "Q" or action == "q":
            helloworld()
            helloworld("Narrator: Leaving so soon? Okay.")
            time.sleep(2)
            exit()
        else:
            helloworld("You can't do that.")
        helloworld("===============================================")
        time.sleep(2)
        self.prompt()

    def introduction(self):
        self.memory = input("Do you usually make good decisions? (Y/N): ")
        pygame.mixer.Sound.play(sfx_select)
        print()
        if self.memory == "N" or self.memory == "n" or self.memory == "Y" or self.memory == "y":
            print("Narrator: Oh hello there-")
            time.sleep(1)
            print("Narrator: Wait... have I seen you before?")
            time.sleep(2)
            self.decide_10puzzles()
        else: 
            print("You must try again.")
            time.sleep(2)
            self.introduction()

    def decide_10puzzles(self):
        print()
        answer = input("Type here to answer his question (Y/N): ")
        print()
        pygame.mixer.Sound.play(sfx_select)
        if answer == "Y" or answer == "y":
            if self.memory == "N" or self.memory == "n":
                print("Narrator: YOU. YOU DESTROYED MY PUZZLES.")
                time.sleep(2)
                print("Narrator: I thought you'd never come back!")
                time.sleep(2)
                print("Narrator: ARRRGGHHHH!!!")
                time.sleep(2)
                print("Narrator: ...Okay... well now you're gonna play my text-based game.")
                time.sleep(2)
                print("Narrator: And this time, you can't break ANYTHING!")
                time.sleep(2)
                helloworld("===============================================")
                self.prompt()
            if self.memory == "Y" or self.memory == "y":
                print("Narrator: I knew it! You are the tester who tested Ten Puzzles!")
                time.sleep(2)
                print("Narrator: Wow, I'd never thought I'd see you again.")
                time.sleep(2)
                print("Narrator: I guess you get to play my text-based game now.")
                time.sleep(2)
                print("Narrator: All you gotta do is follow the instructions.")
                time.sleep(2)
                helloworld("===============================================")
                self.prompt()
        elif answer == "N" or answer == "n":
            print("Narrator: Oh. I guess you just look familiar to me.")
            time.sleep(2)
            print("Narrator: I guess you get to play my text-based game now.")
            time.sleep(2)
            print("Narrator: All you gotta do is follow the instructions.")
            time.sleep(2)
            helloworld("===============================================")
            self.prompt()
        else: 
            print("Narrator: That's... not an answer. Just tell me either Y/N.")
            self.decide_10puzzles()