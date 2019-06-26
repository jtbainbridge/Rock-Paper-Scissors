"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

import random
moves = ['rock', 'paper', 'scissors']

class tcolor:
    WIN = '\033[92m'
    TIE = '\033[93m'
    LOSE = '\033[91m'
    ENDC = '\033[0m'


# INPUT VALIDATION:
def valid_input(prompt, options):
    while True:
        response = input(prompt).lower()
        for option in options:
            if option == response:
                return response
        print("Sorry, I don't understand.")

# HIERARCHY:
def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Player:
    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):
    def move(self):
        choice = valid_input("Rock, Paper or Scissors? > ", moves)
        return choice

# MIRROR THE LAST MOVE PLAYED BY P1:
class ReflectPlayer(Player):
    def __init__(self):
        self.ref_move = random.choice(moves)

    def learn(self, my_move, their_move):
        self.ref_move = their_move

    def move(self):
        return self.ref_move

# P2 MOVE CYCLES THROUGH BASED ON P2 LAST MOVE:
class CyclePlayer(Player):
    def __init__(self):
        self.last_move = None

    def learn(self, my_move, their_move):
        self.last_move = my_move

    def move(self):
        if self.last_move == None:
            return random.choice(moves)
        elif self.last_move == 'rock':
            return 'paper'
        elif self.last_move == 'paper':
            return 'scissors'
        elif self.last_move == 'scissors':
            return 'rock'


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.p1_score = 0
        self.p2_score = 0


    def score(self, move1, move2):
        if beats(move1, move2) is True:
            print("* YOU WON THIS ROUND! *")
            self.p1_score += 1
        elif beats(move2, move1) is True:
            self.p2_score += 1
            print("* YOUR OPPONENT WON THIS ROUND *")
        else:
            print("* TIE *")


    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"You played {move1}.")
        print(f"Oppenent played {move2}.")
        # RECORD MOVES
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        # RUN THE CHECK SCORE FUNCTION:
        self.score(move1, move2)
        # PRINT THE CURRENT SCORE
        print(f"Latest score - You: {self.p1_score}\t Opponent: {self.p2_score}\n")


    def play_game(self):
        self.rounds = int(valid_input("How many rounds would you like to play? (1, 3 or 5) > "
                             , ['1', '3', '5']))
        print("Game start!")
                
        for round in range(self.rounds):
            print(f"--- Round {round +1} of {self.rounds} ---")
            self.play_round()
        print("Game over!")
        self.results()


    def results(self):
        if self.p1_score > self.p2_score:
            print(tcolor.WIN + "** CONGRATULATIONS, YOU WON THE GAME! **" + tcolor.ENDC)
        elif self.p1_score < self.p2_score:
            print(tcolor.LOSE + "** COMMESERATIONS, YOUR OPPONENT WON THE GAME. **" + tcolor.ENDC)
        else:
            print(tcolor.TIE + "** THE GAME IS TIED **" + tcolor.ENDC)
        print(f"FINAL SCORE - You: {self.p1_score}\tOpponent: {self.p2_score}\n")
        self.play_again()
    

    def play_again(self):
        self.restart = valid_input("Would you like to play again? (y/n):\n",
                            ["y", "n"])
        if self.restart == "y":
            print("Great stuff! Resetting the game...\n")
            self.p1_score = 0
            self.p2_score = 0
            print("--NEW GAME--")
            self.play_game()
        elif self.restart == "n":
            print("Thank you for playing. Goodbye.")



if __name__ == '__main__':
    cpu_players = [Player, RandomPlayer, ReflectPlayer, CyclePlayer]
    rand_cpu = random.choice(cpu_players)()
    game = Game(HumanPlayer(), rand_cpu)
    game.play_game()