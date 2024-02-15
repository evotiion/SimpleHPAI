#configs.py=====================================

class Configs():
    def __init__(self):
        self.BOARD_COLS = 8
        self.BOARD_ROWS = 1
        self.POLICIES_DIR = './policies'
        self.lr = 0.2
        self.decay_gamma = 0.9
        self.exp_rate = 0.3
#below seems like a good value to never lose.
        self.training_epoch = 14000
#        self.training_epoch = 10000