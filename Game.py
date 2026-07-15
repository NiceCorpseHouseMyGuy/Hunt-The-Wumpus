## This imports the classes from other files or modules ##

from Player import Player
from Wumpus import Wumpus
from Ravens import Ravens
from Cavern import Cavern
from Map import Map
import time
import pygame
import random

# sounds aren't really necessary but fun.

pygame.init()
pygame.mixer.init()

sfx_select = pygame.mixer.Sound('sounds/select.ogg')
sfx_prompt = pygame.mixer.Sound('sounds/prompt.ogg')
sfx_gameover = pygame.mixer.Sound('sounds/gameover.ogg')

## The Main Game Class ##

class Game:
    ## This gets all the classes imported and put into their respective variables ##
    def __init__(self):
        self.Player = Player()
        self.Wumpus = Wumpus()
        self.Ravens1 = Ravens()
        self.Ravens2 = Ravens()
        self.RavensList = [self.Ravens1, self.Ravens2]
        self.Cavern1 = Cavern()
        self.Cavern2 = Cavern()
        self.CavernList = [self.Cavern1, self.Cavern2]
        self.memory = None
        self.map = Map()

    ## This sets the positions of the Player, the Ravens, and the Caverns ##
    def set_positions(self):
        self.map.occupied.clear()
        self.map.player_occupied.clear()

        self.Player.position = random.randint(1, 12)
        self.map.occupied.append(self.Player.position) # This sets the room occupied.
        self.map.set_unoccupied() # This removes occupied rooms from the list of unoccupied rooms.

        # This is here so that the Wumpus doesn't spawn around the player by getting the rooms around the player and the rooms everything is in.
        self.map.player_occupied.append(self.Player.position)
        self.map.occupied.extend(self.map.rooms[self.Player.position])
        self.map.set_player_unoccupied()

        for raven in self.RavensList:
            raven.position = random.choice(self.map.unoccupied) # This is here to set the position to a room unoccupied.
            self.map.occupied.append(raven.position)
            self.map.set_unoccupied()

        for cavern in self.CavernList:
            cavern.position = random.choice(self.map.unoccupied)
            self.map.occupied.append(cavern.position)
            self.map.set_unoccupied()

        self.Wumpus.position = random.choice(self.map.player_occupied)

    ## This is just the title ##
    def begin_game(self):
        print("     ( This game also has sound effects  )     ")
        print("     ( As well as a sequel to 10 Puzzles )     ")
        print("===============================================")
        print("                The Blind Hunt                 ")
        print("===============================================")
        self.introduction()

    ## This basically shows what you will expect and resets things when you retry the game ##
    def opening(self):
        self.Player.alive = True
        self.Player.arrows = 5
        self.set_positions()
        print("You've been dropped into a random cave.")
        time.sleep(2)
        print("You have five arrows.")
        time.sleep(2)
        print("It will run if you miss.")
        time.sleep(2)
        print("Don't fall.")
        time.sleep(2)
        print("Avoid the Ravens.")
        time.sleep(2)
        print("Hunt The Wumpus.")
        time.sleep(2)
        print("===============================================")
        self.prompt()

    ## This is where you choose your next action. ##
    def prompt(self):
        pygame.mixer.Sound.play(sfx_prompt)
        print("              Choose Your Action               ")
        print("===============================================")
        print(f"You are in Room {self.Player.position}")
        print(f"Possible Paths: {self.map.rooms[self.Player.position]}")
        print()
        self.check_near_dangers()
        print("Your options are: (M)ove or (S)hoot or (Q)uit.")
        print(f"You have {self.Player.arrows} Arrows left.")
        print()
        action = input("What is your next action?: ")
        pygame.mixer.Sound.play(sfx_select)
        if action in ["M", "m"]:
            self.select_path()
        elif action in ["S", "s"]:
            self.shoot_arrow()
        elif action in ["Q", "q"]:
            print()
            print("Narrator: Leaving so soon? Okay.")
            time.sleep(2)
            exit()
        else:
            print("You can't do that.")
            time.sleep(2)
            print("===============================================")
            self.prompt()

    ## This checks if you are near any danger when you're choosing your next action ##
    def check_near_dangers(self):
        if self.Player.position in self.map.rooms[self.Wumpus.position]:
            print("You hear breathing.")
            print()
        for raven in self.RavensList:
            if self.Player.position in self.map.rooms[raven.position]:
                print("You hear flapping.")
                print()
                break
        for cavern in self.CavernList:
            if self.Player.position in self.map.rooms[cavern.position]:
                print("You feel a breeze.")
                print()

    ## If you chose to move, you must select the path ##
    def select_path(self):
        time.sleep(0.2)
        pygame.mixer.Sound.play(sfx_prompt)
        selected_path = input("Enter Room: ")
        try: 
            selected_path = int(selected_path)
            pygame.mixer.Sound.play(sfx_select)
            time.sleep(0.2)
            if selected_path in self.map.rooms[self.Player.position]:
                self.Player.position = selected_path
                self.map.set_unoccupied()
                # These are here to check what is in the room you wanna go to before you can safely be there.
                self.check_wumpus()
                self.check_ravens()
                self.check_caverns() 
                if self.Player.alive == True:
                    # If nothing is here, then you will be safe.
                    print("===============================================")
                    self.prompt()
            else: 
                print("This is not an available room.")
                print("===============================================")
                self.prompt()

        except ValueError: # The reason this is here is because if you ever try to type in anything that's not a number, it will crash.
            print("This is not a room.")
            print("===============================================")
            self.prompt()

    ## This checks what is in the room you want to go to ##
    def check_wumpus(self):
        if self.Player.alive == True:
            if self.Player.position == self.Wumpus.position: # If the Wumpus is here.
                pygame.mixer.Sound.play(sfx_gameover)
                self.Player.alive = False
                time.sleep(0.5)
                print("===============================================")
                print("           THE WUMPUS HAS FOUND YOU            ")
                print("===============================================")
                time.sleep(3)
                self.try_again()

    def check_ravens(self):
        for raven in self.RavensList:
            if self.Player.position == raven.position: # If the Ravens are here.
                self.Player.alive = False
                time.sleep(0.5)
                print("===============================================")
                print("       You've been displaced by Ravens!        ")
                print("===============================================")
                self.Player.position = random.choice(self.map.unoccupied)
                time.sleep(3)
                self.Player.alive = True
                self.prompt()

    def check_caverns(self):
        for cavern in self.CavernList:
            if self.Player.position == cavern.position: # If the Cavern is here.
                pygame.mixer.Sound.play(sfx_gameover)
                self.Player.alive = False
                time.sleep(0.5)
                print("===============================================")
                print("            YOU FELL INTO A CAVERN             ")
                print("===============================================")
                time.sleep(3)
                self.try_again()

    ## This shoots arrows as well as tells you when you win the game ##
    def shoot_arrow(self):
        time.sleep(0.2)
        if self.Player.arrows > 0: # You can't shoot arrows you don't have.
            pygame.mixer.Sound.play(sfx_prompt)
            selected_path = input("Shoot Room: ")
            try:
                selected_path = int(selected_path)
                pygame.mixer.Sound.play(sfx_select)
                self.Player.shoot_arrow()
                if self.Player.position in self.map.rooms[self.Wumpus.position]:
                    if selected_path == self.Wumpus.position:
                        ## This is basically where you win the game. ##
                        print()
                        print("Wumpus: You shot me...")
                        time.sleep(2)
                        print("Wumpus: You shot me pretty good.") 
                        time.sleep(2)
                        print()
                        print("===============================================")
                        print("            YOU HUNTED THE WUMPUS              ")
                        print("===============================================")
                        time.sleep(2)
                        self.try_again()
                    else: 
                        print("You missed it! Now it has moved!")
                        self.move_wumpus()
                        time.sleep(2)
                        print("===============================================")
                        self.prompt()

                elif selected_path not in self.map.rooms[self.Player.position]:
                    print("You wasted your arrow on a wall!")
                    time.sleep(2)
                    print("===============================================")
                    self.prompt()

                else:
                    print("There's nothing there...")
                    time.sleep(2)
                    print("===============================================")
                    self.prompt()

            except ValueError:
                print("This is not a room.")
                print("===============================================")
                self.prompt()
        
        else:
            print("You're out of arrows!")
            time.sleep(2)
            print("===============================================")
            self.prompt()

    def move_wumpus(self):
        self.Wumpus.position = random.choice(self.map.unoccupied)

    ## This appears when you die ##
    def try_again(self):
        answer = input("(R)etry or (Q)uit: ")
        pygame.mixer.Sound.play(sfx_select)
        if answer in ["R", "r"]:
            print("===============================================")
            self.opening()
        elif answer in ["Q", "q"]:
            print()
            print("Narrator: Leaving so soon? Okay.")
            time.sleep(2)
        else:
            print()
            print("This is not an option.")
            time.sleep(2)
            self.try_again()

    ## This is the first part of the reintroduction of the narrator and yourself from 10 Puzzles ##
    def introduction(self):
        pygame.mixer.Sound.play(sfx_prompt)
        self.memory = input("Do you usually make good decisions? (Y/N) (S)kip: ")
        pygame.mixer.Sound.play(sfx_select)
        print()
        if self.memory in ["N", "n", "Y", "y"]:
            print("Narrator: Oh hello there-")
            time.sleep(1)
            print("Narrator: Wait... have I seen you before?")
            time.sleep(2)
            self.decide_10puzzles()
        elif self.memory == "S" or self.memory == "s": # Skipping is here for convenience.
            time.sleep(0.2)
            print("===============================================")
            self.opening()
        else: 
            print("You must try again.")
            time.sleep(2)
            self.introduction()

    ## The second part of the reintroduction whether if you've played 10 Puzzles or not.
    def decide_10puzzles(self):
        time.sleep(0.2)
        pygame.mixer.Sound.play(sfx_prompt)
        print()
        answer = input("Type here to answer his question (Y/N): ")
        print()
        pygame.mixer.Sound.play(sfx_select)
        if answer in ["Y", "y"]:
            if self.memory in ["N", "n"]:
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
                print("Narrator: I think...")
                time.sleep(1)
                print("===============================================")
                self.opening()
            if self.memory in ["Y", "y"]:
                print("Narrator: I knew it! You are the tester who tested Ten Puzzles!")
                time.sleep(2)
                print("Narrator: Wow, I'd never thought I'd see you again.")
                time.sleep(2)
                print("Narrator: I guess you get to play my text-based game now.")
                time.sleep(2)
                print("Narrator: All you gotta do is follow the instructions.")
                time.sleep(2)
                print("===============================================")
                self.opening()
        elif answer in ["N", "n"]:
            print("Narrator: Oh. I guess you just look familiar to me.")
            time.sleep(2)
            print("Narrator: I guess you get to play my text-based game now.")
            time.sleep(2)
            print("Narrator: All you gotta do is follow the instructions.")
            time.sleep(2)
            print("===============================================")
            self.opening()
        else: 
            print("Narrator: That's... not an answer. Just tell me either Y/N.")
            self.decide_10puzzles()