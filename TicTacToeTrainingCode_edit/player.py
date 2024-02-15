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
        # specific for training-----------------------------------------------
        self.lr = self.configs.lr
        self.decay_gamma = self.configs.decay_gamma
        self.exp_rate = self.configs.exp_rate
        self.states = []
        self.states_val = {}

    def getHash(self, board):
        reshapedBoard = board.reshape(self.BOARD_ROWS * self.BOARD_COLS)
        #        print("board")
        #        print(board)
        #        print("reshape")
        #        print (reshapedBoard)
        return str(reshapedBoard)

    # specific for training-----------------------------------------------
    def chooseAction(self, positions, board, playerSymbol):
        # choose randomly
        if (np.random.uniform(0, 1, 1) <= self.exp_rate) or (len(self.states_val) == 0.):
            idx = np.random.choice(len(positions))
            action = positions[idx]


        # exploitation using greedy method
        else:
            max_value = -999
            for p in positions:

                tmp_board = board.copy()
                tmp_board[p] = playerSymbol
                tmp_hashBoard = self.getHash(tmp_board)

                value = 0 if self.states_val.get(tmp_hashBoard) is None else self.states_val.get(tmp_hashBoard)

                """
                if self.states_val.get(tmp_hashBoard) is None:
                    value = 0
                else:
                    value = self.states_val.get(tmp_hashBoard)
                """

                if value > max_value:
                    max_value = value
                    action = p

        return action

    def addStates(self, board_hash):
        self.states.append(board_hash)

    #        print(self.states)

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_val.get(st) is None:
                self.states_val[st] = 0

            self.states_val[st] += self.lr * (self.decay_gamma * reward - self.states_val[st])
            reward = self.states_val[st]

    # ---------------------------------------------------------------

    def reset(self):
        self.states = []

    def savePolicy(self, path):
        fw = open(os.path.join(path, 'policy_' + str(self.name)), 'wb')
        pickle.dump(self.states_val, fw)
        fw.close()
