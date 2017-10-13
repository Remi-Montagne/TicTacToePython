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
import minimax as mn

########################################
#              CLASSES
########################################

class Match:
    """A class to do several games of tic-tac-toe"""
    def __init__(self):
        """Initiate a mtch between player 1 and player 2.
        Score is in a dictionary.
        """
        self.opponent = self.get_opponent()
        self.player1 = self.get_player("X")
        self.player2 = self.get_player("O") if self.opponent == 1 else "Ordinateur"
        self.scores = [0, 0]
        self.continue_match = True
    
    def get_opponent(self):
        print('############################################################\
        \n\tBienvenue dans le jeu du morpion !\
        \nVoulez-vous jouer contre une autre personne ou l\'ordinateur ?\
        \n1 pour un adversaire humain\
        \n2 pour l\'ordinateur')
        while True:
            inpt = input()
            if inpt not in ['1', '2']:
                print("Je ne comprends pas cette réponse.")
            else:
                return int(inpt)

    def get_player(self, nb):
        """Get the name of the players"""
        return input('Joueur {}: '.format(nb))
    
    def play_match(self):
        """The steps of the match"""
        while self.continue_match:
            my_grid = Grid(self.player1, self.player2, self.opponent)
            self.update_score(my_grid.play())
            self.continue_match = self.another_game()
        self.final_result()
        
    def update_score(self, winner):
        """Once a game has been played, update the final score"""
        if winner != -1: self.scores[winner] += 1

    def another_game(self):
        """Ask the players if they want to play one more game"""
        print('{0}: {1} - {2}: {3}'.format(self.player1, self.scores[0], self.player2, self.scores[1]))
        while True:
            res = input('Faire une autre partie (Y, N) ? ').upper()
            if res == 'Y' :
                return True
            elif res == 'N':
                return False
            else:
                print("Je n'ai pas compris la réponse.")

    def final_result(self):
        """Print the results of the global match"""
        if self.scores[0] > self.scores[1]:
            print('{} est le grand gagnant. Félicitation !'.format(self.player1))
        elif self.scores[0] < self.scores[1]:
            print('{} est le grand gagnant. Félicitation !'.format(self.player2))
        else:
            print('Match nul. Bravo à tous les 2 !')


class Position:
    
    def __init__(self, i, j):
        self.line = i
        self.col = j


class Grid:
    """ The class for the tic-tac-toe grid.
    Here player1 is referred to as 1 and player2 as -1.
    Grid is an abstract class. Its children are GridHumanAgainstHuman
    and GridHumanAgainsComputer. They implement different version of
    the method play.
    """

    EMPTY_CASE = """|_|"""
    O_CASE = """|O|"""
    X_CASE = """|X|"""

    def __init__(self, player1, player2, opponent):
        """initiation of the grid"""
        self.grid = np.zeros((3,3))
        self.players = [player1, player2]
        self.opponent = opponent
        self.current_player = self.get_first_player()
        self.player_scores = [1, -1]
        self.winner = -1
        self.continue_game = True
    
    def play(self):
        """The succession of steps of a game"""
        print(self)
        while self.continue_game:
            #get the case to mark
            if self.current_player == 0:
                position = self.get_case()
            else:
                if self.opponent == 1:
                    position = self.get_case()
                if self.opponent == 2:
                    pos, score = mn.mini_max(self.grid)
                    position = Position(pos[0], pos[1])

            #if the player entered "stop", stop the game
            if position.line == -1 or position.col == -1 : break
                        
            #mark the case
            self.mark_case(position, self.current_player)
            
            #process the end of turn
            print(self)
            self.check_grid()
            self.change_player()
            
        print(self.end_of_game_message())
        return self.winner

    def get_first_player(self):
        """Get the name of the players who begins"""
        keep_going = True
        while keep_going:
            inpt = input('Choisissez qui commence: \
            \n1 pour {0}\
            \n2 pour {1}\
            \n3 pour choisir au hasard\n'.format(self.players[0], self.players[1]))
            if inpt not in ['1', '2', '3']:
                print("Je ne comprends pas cette réponse.")
            elif inpt == '3':
                res = rd.randint(0, 1)
                keep_going = False
            else:
                res = int(inpt) - 1
                keep_going = False
        return res

    def get_case(self):
        """Get the case to mark."""
        #indicate the player whose turn it is
        print('{} choisit une case'.format(self.players[self.current_player]) \
        + '("stop" to quit):')
        
        free_case = False
        while not free_case :
            line = self.player_input('ligne')
            if line == -1: return Position(-1, -1)

            col = self.player_input('colonne')
            if col == -1: return Position(-1, -1)

            if self.grid[line, col] == 0 :
                return Position(line, col)
            else:
                print('Cette case a déjà été marquée. Choisissez-en une autre')

    def player_input(self, word) :
        """Get the line or colomn that the player wants to mark."""
        while True:
            res = input('  {} (1, 2, ou 3): '.format(word))
            if res == 'stop':
                return -1
            elif res not in ['1', '2', '3']: 
                print('Cette valeur n\'est pas possible.')
            else:
                return int(res)-1

    def mark_case(self, position, current_player):
        """Mark a case in the grid."""
        self.grid[position.line, position.col] = self.player_scores[current_player]

    def check_grid(self):
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
            self.winner = 0
        elif -3 in self.grid.sum(axis = 0) or -3 in self.grid.sum(axis = 1) \
        or self.grid.trace() == -3 or trace_inverse == -3 :
            self.continue_game = False
            self.winner = 1

    def change_player(self):
        self.current_player = 1 if self.current_player == 0 else 0

    def end_of_game_message(self):
        list_messages = ["Match nul.",
        "{} gagne cette manche.".format(self.players[self.winner]),
        "{} gagne cette manche".format(self.players[self.winner])
        ]
        return list_messages[self.winner+1]

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


class GridHumanAgainstHuman(Grid):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)


class GridHumanAgainstComputer(Grid):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)

    def play(self):
        """The succession of steps of a game"""
        print(self)
        while self.continue_game:
            if self.current_player == 0:
                #get the case to mark
                position = self.get_case()
                if position.line == -1 or position.col == -1 : break
                            
                #mark the case
                self.mark_case(position, self.current_player)
                
                #process the end of turn
                print(self)
                self.check_grid()
                self.change_player()
            else:
                #get the case to mark
                move, score = mn.mini_max(self.grid)
                if position.line == -1 or position.col == -1 : break
                            
                #mark the case
                self.mark_case(position, self.current_player)
                
                #process the end of turn
                print(self)
                self.check_grid()
                self.change_player()

        print(self.end_of_game_message())
        return self.winner
    
########################################
#                MAIN
########################################

def main() :
    my_match = Match()
    my_match.play_match()


if __name__ == "__main__" :
    main()
