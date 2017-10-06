#! /usr/bin/env python3
# coding : utf-8

"""
This program code a standard tic-tac-toe game for 2 players
"""

########################################
#              MODULES
########################################

import os
from sys import exit
import random as rd
import numpy as np

########################################
#              CLASSES
########################################

class Grid:
    """ The class for the tic-tac-toe grid.
    Here player1 is referred to as 1 and player2 as -1.
    """

    EMPTY_CASE = """|_|"""
    O_CASE = """|O|"""
    X_CASE = """|X|"""
    PLAYERS = [] 
    SCORES = [0, 0]
    FIRST_TO_PLAY = -1
    CONTINUE_MATCH = True
    
    @classmethod
    def init_match(cls):
        cls.PLAYERS.append(cls.get_player("X")) 
        cls.PLAYERS.append(cls.get_player("O"))
        cls.FIRST_TO_PLAY = cls.get_first_player()

    def __init__(self):
        """initiation of the grid"""
        self.grid = np.zeros((3,3))
        self.current_player = self.FIRST_TO_PLAY
        self.player_scores = [1, -1]
        self.winner = -1
        self.continue_game = True

    @classmethod
    def get_player(cls, nb):
        """Get the name of the players"""
        return input('Joueur {}: '.format(nb))
    
    @classmethod
    def get_first_player(cls):
        """Get the name of the players who begins"""
        res = ""
        while res not in [1, 2, 3]:
            res = int(input("""Choisissez qui commence:
1 pour {0}
2 pour {1}
3 pour choisir au hasard\n""".format(cls.PLAYERS[0], cls.PLAYERS[1])))
            if res not in [1, 2, 3]: 
                print("Je ne comprends pas cette réponse.")
            elif res == 3: 
                res = rd.randint(1, 2)
        res -= 1
        return res

    @classmethod
    def play_match(cls):
        """The steps of the match"""
        while cls.CONTINUE_MATCH:
            my_grid = Grid()
            winner = my_grid.play()
            cls.update_score(winner)
            cls.another_game()
            cls.choose_next_beginner(winner)
        cls.final_result()
    
    @classmethod
    def update_score(cls, winner):
        """Once a game has been played, update the final score"""
        if winner != -1: cls.SCORES[winner] += 1
    
    @classmethod
    def another_game(cls):
        """Ask the players if they want to play one more game"""
        print('{0}: {1} - {2}: {3}'.format(cls.PLAYERS[0], cls.SCORES[0], cls.PLAYERS[1], cls.SCORES[1]))
        correct_answer = False
        while not correct_answer :
            res = input('Faire une autre partie (Y, N) ? ').upper()
            if res == 'Y' :
                correct_answer = True
                cls.CONTINUE_MATCH = True
            elif res == 'N':
                correct_answer = True
                cls.CONTINUE_MATCH = False
            else:
                print("Je n'ai pas compris la réponse.")

    @classmethod
    def choose_next_beginner(cls, winner):
        """If the somebody won the previous game, the other player begins.
        Else, it is the player who didn't begin last time.
        """
        if winner == 0:
            cls.FIRST_TO_PLAY = 1
        elif winner == 1:
            cls.FIRST_TO_PLAY = 0
        else:
            cls.FIRST_TO_PLAY = (cls.FIRST_TO_PLAY + 1) % 2

    @classmethod
    def final_result(cls):
        """Print the results of the global match"""
        if cls.SCORES[0] > cls.SCORES[1]:
            print('{} est le grand gagnant. Félicitation !'.format(cls.PLAYERS[0]))
        elif cls.SCORES[0] < cls.SCORES[1]:
            print('{} est le grand gagnant. Félicitation !'.format(cls.PLAYERS[1]))
        else:
            print('Match nul. Bravo à tous les 2 !')

    def play(self):
        """The succession of steps of a game"""
        if self.SCORES[0] + self.SCORES[1] != 0: print('\nCette fois-ci, {} commence'.format(self.PLAYERS[self.FIRST_TO_PLAY]))
        print(self)
        while self.continue_game:
            #indicate the player whose turn it is
            print('{} choisit une case'.format(self.PLAYERS[self.current_player])
            + '("stop" to quit):')
            #get the case to mark
            line, col = self.get_case()
            if line == -1 or col == -1 : return -1            
            #mark the case
            self.mark_case(line, col, self.player_scores[self.current_player])
            #process the end of turn
            print(self)
            self.continue_game = self.play_again()
            if self.continue_game : self.change_player()
        
        print(self.end_of_game_message())
        return self.winner

    def get_case(self):
        """Get the case to mark."""
        free_case = False
        while not free_case :
            line = self.player_input('ligne')
            if line == -1: return (-1, -1)

            col = self.player_input('colonne')
            if col == -1: return (-1, -1)

            if self.grid[line, col] == 0 :
                free_case = True
                return line, col
            else:
                print('Cette case a déjà été marquée. Choisissez-en une autre')

    def player_input(self, word) :
        """Get the line or colomn that the player wants to mark."""
        res = ''
        while res not in ['1', '2', '3', 'stop'] :
            res = input('  {} (1, 2, ou 3): '.format(word))
            if res == 'stop':
                return -1
            elif res not in ['1', '2', '3']: 
                print('Cette valeur n\'est pas possible.')
            else:
                return int(res)-1

    def mark_case(self, line, col, player):
        """Mark a case in the grid."""
        self.grid[line, col] = player

    def play_again(self):
        """Check if the game must continue or stop and if 
        someone won"""
        #check if their is any case left. If not, stop the game.
        res = False
        for line in range(3) :
            for col in range(3) :
                if self.grid[line, col] == 0:
                    res = True

        #check if a player made a line. If yes, stop the game.            
        trace_inverse = self.grid[2, 0] + self.grid[1, 1] + self.grid[0, 2]

        if 3 in self.grid.sum(axis = 0) or 3 in self.grid.sum(axis = 1) \
        or self.grid.trace() == 3 or trace_inverse == 3 : 
            res = False
            self.winner = 0
        elif -3 in self.grid.sum(axis = 0) or -3 in self.grid.sum(axis = 1) \
        or self.grid.trace() == -3 or trace_inverse == -3 :
            res = False
            self.winner = 1
        return res
    
    def change_player(self):
        self.current_player = 1 if self.current_player == 0 else 0

    def end_of_game_message(self):
        list_messages = ["Match nul.",
        "{} gagne cette manche.".format(self.PLAYERS[self.winner]),
        "{} gagne cette manche".format(self.PLAYERS[self.winner])
        ]
        return list_messages[self.winner + 1]

    def __repr__(self):
        res = ""
        for line in range(3):
            for col in range(3):
                if self.grid[line,col] == 0:
                    res = res + Grid.EMPTY_CASE.rstrip('\n')
                elif self.grid[line,col] == 1:
                    res = res + Grid.X_CASE.rstrip('\n')
                else:
                    res = res + Grid.O_CASE.rstrip('\n')
            res = res + "\n"
        return res


########################################
#                MAIN
########################################

def main() :
    my_match = Grid.init_match()
    Grid.play_match()

if __name__ == "__main__" :
    main()
