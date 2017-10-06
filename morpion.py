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

class Match:
    """A class to do several games of tic-tac-toe"""
    def __init__(self):
        """Initiate a mtch between player 1 and player 2.
        Score is in a dictionary.
        """
        self.player1 = self.get_player("X")
        self.player2 = self.get_player("O")
        self.first = self.get_first_player()
        self.scores = {
                        self.player1: 0, 
                        self.player2: 0
                        }
        self.continue_match = True
    
    def get_player(self, nb):
        """Get the name of the players"""
        return input('Joueur {}: '.format(nb))
    
    def get_first_player(self):
        """Get the name of the players who begins"""
        res = ""
        while res not in [1, 2, 3]:
            res = int(input("""Choisissez qui commence:
1 pour {0}
2 pour {1}
3 pour choisir au hasard\n""".format(self.player1, self.player2)))
            if res not in [1, 2, 3]: 
                print("Je ne comprends pas cette réponse.")
            elif res == 2: 
                self.switch(self.player1, self.player2)
            elif res == 3: 
                res = rd.randint(1, 2)
        return res
    
    def switch(self, player1, player2):
        self.player1 = player2
        self.player2 = player1
    
    def play_match(self):
        """The steps of the match"""
        while self.continue_match:
            my_grid = Grid(self.player1, self.player2)
            self.update_score(my_grid.play())
            self.another_game()
        self.final_result()
        
    def update_score(self, winner):
        """Once a game has been played, update the final score"""
        if winner == 1:
            self.scores[self.player1] += 1
        elif winner == 2:
            self.scores[self.player2] += 1
            return 0
        
    def another_game(self):
        """Ask the players if they want to play one more game"""
        print('{0}: {1} - {2}: {3}'.format(self.player1, self.scores[self.player1], self.player2, self.scores[self.player2]))
        correct_answer = False
        while not correct_answer :
            res = input('Faire une autre partie (Y, N) ? ').upper()
            if res == 'Y' :
                correct_answer = True
                self.continue_match = True
            elif res == 'N':
                correct_answer = True
                self.continue_match = False
            else:
                print("Je n'ai pas compris la réponse.")

    def final_result(self):
        """Print the results of the global match"""
        if self.scores[self.player1] > self.scores[self.player2]:
            print('{} est le grand gagnant. Félicitation !'.format(self.player1))
        elif self.scores[self.player1] < self.scores[self.player2]:
            print('{} est le grand gagnant. Félicitation !'.format(self.player2))
        else:
            print('Match nul. Bravo à tous les 2 !')

class Grid:
    """ The class for the tic-tac-toe grid.
    Here player1 is referred to as 1 and player2 as -1.
    """

    EMPTY_CASE = """|_|"""
    O_CASE = """|O|"""
    X_CASE = """|X|"""

    def __init__(self, player1, player2):
        """initiation of the grid"""
        self.grid = np.zeros((3,3))
        self.current_player = 0
        self.player_names = [player1, player2]
        self.player_scores = [1, -1]
        self.winner = 0
        self.continue_game = True
    
    def play(self):
        """The succession of steps of a game"""
        print(self)
        while self.continue_game:
            #indicate the player whose turn it is
            print('{} choisit une case'.format(self.player_names[self.current_player])
            + '("stop" to quit):')
            #get the case to mark
            line, col = self.get_case()
            if line == -1 or col == -1 : break            
            #mark the case
            self.mark_case(line, col, self.player_scores[self.current_player])
            #process the end of turn
            print(self)
            self.play_again()
            if self.play_again : self.change_player()
            
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
        self.continue_game = False
        for line in range(3) :
            for col in range(3) :
                if self.grid[line, col] == 0:
                    self.continue_game = True

        #check if a player made a line. If yes, stop the game.            
        trace_inverse = self.grid[2, 0] + self.grid[1, 1] + self.grid[0, 2]
        
        if 3 in self.grid.sum(axis = 0) or 3 in self.grid.sum(axis = 1) \
        or self.grid.trace() == 3 or trace_inverse == 3 : 
            self.continue_game = False
            self.winner = 1
        elif -3 in self.grid.sum(axis = 0) or -3 in self.grid.sum(axis = 1) \
        or self.grid.trace() == -3 or trace_inverse == -3 :
            self.continue_game = False
            self.winner = 2

    def change_player(self):
        self.current_player = 1 if self.current_player == 0 else 0

    def end_of_game_message(self):
        list_messages = ["Match nul.",
        "{} gagne cette manche.".format(self.player_names[self.winner -1]),
        "{} gagne cette manche".format(self.player_names[self.winner -1])
        ]
        return list_messages[self.winner]

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
    my_match = Match()
    my_match.play_match()


if __name__ == "__main__" :
    main()
