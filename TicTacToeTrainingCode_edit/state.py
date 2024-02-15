import numpy as np

from configs import Configs


class State():
    def __init__(self, p1, p2):
        self.configs = Configs()
        self.BOARD_COLS = self.configs.BOARD_COLS
        self.BOARD_ROWS = self.configs.BOARD_ROWS
        self.POLICIES_DIR = self.configs.POLICIES_DIR

        self.p1 = p1
        self.p2 = p2

        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def getHash(self):
        self.boardHash = str(self.board.reshape(self.BOARD_ROWS * self.BOARD_COLS))
        return self.boardHash

    def getAvailablePositions(self):
        positions = []
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                if self.board[i][j] == 0:
                    positions.append((i, j))

        return positions

    def winner(self):
        """
        Values on board: Player 1: 1 || Player 2: -1
        To check if there is a winner/draw
        """
        p1Score = 0
        p2Score = 0
        multi = 1
        if len(self.getAvailablePositions()) == 0:

            for j in range(self.BOARD_COLS):
                if self.board[0, j] == 1:
                    p1Score += j
                elif self.board[0, j] == -1:
                    p2Score += j

            self.isEnd = True

            print("p1Score is " + str(p1Score))
            print("p2Score is " + str(p2Score))

            if p1Score != 0:
                multi = ((p1Score/p2Score)/100)+1

            if p1Score > p2Score:
                return 1, multi
            elif p2Score > p1Score:
                return -1, multi
            elif p1Score == p2Score:
                return 0, multi

        # game continues
        self.isEnd = False
        return None, 1

    def updateStates(self, position):
        self.board[position] = self.playerSymbol

        # Switch player
        self.playerSymbol = 1 if self.playerSymbol == -1 else -1

    def reset(self):
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    # specific for training-----------------------------------------------
    def giveReward(self):
        """
        At game end only
        """
        result, multi = self.winner()
        self.showBoard()
        print("Multi is " + str(multi))
        print("Winner is " + str(result))

        if result == 1:
            self.p1.feedReward(1*multi)
            self.p2.feedReward(0)

        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)

        else:
            # if its a draw
            self.p1.feedReward(0.1)  # less reward
            self.p2.feedReward(0.5)  # to make p1 more aggressive

    # specific for training-----------------------------------------------
    # play between bots
    def playGame(self, rounds=100):
        print("Initialize training for {} epochs".format(rounds))
        for i in range(rounds):
            if i % 1000 == 0:
                print('Rounds {}'.format(i))

            while not self.isEnd:
                # player 1
                positions = self.getAvailablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                self.updateStates(p1_action)
                board_hash = self.getHash()
                self.p1.addStates(board_hash)
                #self.showBoard()

                # check if win
                winner, multi = self.winner()


                if winner is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # player 2
                    positions = self.getAvailablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateStates(p2_action)
                    board_hash = self.getHash()
                    #                    print(board_hash)
                    self.p2.addStates(board_hash)
                    #self.showBoard()

                    winner, multi = self.winner()

                    if winner is not None:
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

        print("Done training... Saving 2 policies to {}".format(self.POLICIES_DIR))
        self.p1.savePolicy(self.POLICIES_DIR)
        self.p2.savePolicy(self.POLICIES_DIR)

    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, self.BOARD_ROWS):
            print('--0---1---2---3---4---5---6---7--')
            out = '| '
            for j in range(0, self.BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('---------------------------------')