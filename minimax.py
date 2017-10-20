#! /usr/bin/env python3
# coding : utf-8

"""
This program code an algorithm for a tic-tac-toe game against the computer
"""
########################################
#             MODULES
########################################

import random as rd
import numpy as np

########################################
#              FUNCTIONS
########################################

def mini_max(grid, i=0, j=0, active_player=-1, depth=0):
    """The minimax recursive algorithm"""
    moves = []
    scores = []
    depth +=1
    #check the possible next moves for the grid.
    possible_next_moves = get_possible_next_moves(grid)
    #if there is game over (i.e. grid full or a player wins), returns the corresponding score
    if game_over(possible_next_moves, grid):
        return (i, j), get_score(grid, depth)
    #else, a list of possible next moves and associated scores is recursively generated.
    #given the active player, the max or min score and associated move will then be returned.
    else:
        #print('uncomplete grid')
        next_player = other_player(active_player)
        for (i, j) in possible_next_moves:
            moves.append((i, j))
            possible_grid = get_next_possible_grid(grid, i, j, active_player)
            move, score = mini_max(possible_grid, i, j, next_player, depth)
            scores.append(score)
    return get_score_to_return(moves, scores, active_player)

def get_possible_next_moves(grid):
    """Gets the possible next moves given the current grid."""
    possible_moves = []
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[i, j] == 0:
                possible_moves.append((i, j))
    return possible_moves

def game_over(possible_next_moves, grid) :
    """Returns True if a player wins or if the grid is full."""
    if not possible_next_moves or winner(grid) != 0:
        return True
    else:
        return False

def other_player(active_player):
    """Gets the other player."""
    if active_player == 1:
        return -1
    else:
        return 1

def get_next_possible_grid(grid, i, j, active_player):
    possible_grid = np.copy(grid)
    possible_grid[i][j] = active_player
    return possible_grid

def get_score(grid, depth):
    """Calculates the score of a state."""
    if winner(grid) == -1:
        return 10 - depth
    elif winner(grid) == 1:
        return depth -10
    else:
        return 0

def winner(grid):
    """Checks and indicates if the player or the computer made a line.
    Return 1 if the player did and -1 if the computer did.
    """
    trace_inverse = grid[2, 0] + grid[1, 1] + grid[0, 2]

    if 3 in grid.sum(axis=0) or 3 in grid.sum(axis=1) \
    or grid.trace() == 3 or trace_inverse == 3:
        return 1
    elif -3 in grid.sum(axis=0) or -3 in grid.sum(axis=1) \
    or grid.trace() == -3 or trace_inverse == -3:
        return -1
    else:
        return 0

def get_score_to_return(moves, scores, active_player):
    if active_player == -1:
        i = scores.index(max(scores))
    else:
        i = scores.index(min(scores))
    return moves[i], scores[i]


########################################
#                MAIN
########################################

def main():
    test_grid = np.array([[0, 1, 0], [0, 0, 1], [-1, -1, 1]])
    print('Choisir le coup {}'.format(mini_max(test_grid)))

if __name__ == '__main__':
    main()
