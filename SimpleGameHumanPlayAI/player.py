import numpy as np
import pickle
import os

from configs import Configs

class BotPlayer():
    def __init__(self, name):
        self.configs = Configs()
        self.BOARD_COLS = self.configs.BOARD_COLS
        self.BOARD_ROWS = self.configs.BOARD_ROWS

        self.name = name
#        self.lr = self.configs.lr
#        self.decay_gamma = self.configs.decay_gamma
#        self.exp_rate = self.configs.exp_rate

        self.states = []
        self.states_val = {}

    def getHash(self, board):
        return str(board.reshape(self.BOARD_ROWS * self.BOARD_COLS))

#specific to bot----------------------
    def chooseAction(self, positions, board, playerSymbol):
         max_value = -999
         for p in positions:
             tmp_board = board.copy()
             tmp_board[p] = playerSymbol
             tmp_hashBoard = self.getHash(tmp_board)

             value = 0 if self.states_val.get(tmp_hashBoard) is None else self.states_val.get(tmp_hashBoard)

             if value > max_value:
                 max_value = value
                 action = p

         return action
#-----------------------

    def addStates(self, board_hash):
        self.states.append(board_hash)

    def reset(self):
        self.states = []


#specific to bot-------------------------------
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_val = pickle.load(fr)
        fr.close()

#///////////////////////////////////////////////////////////////////////
class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions):
        while True:
            col = input("Input your action: col:")
            action = (0, int(col))

            if action in positions:
                return action

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass
