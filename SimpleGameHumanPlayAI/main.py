import numpy as np
import pickle
import argparse
import os

from state import State
from player import BotPlayer, HumanPlayer
from configs import Configs

#parser = argparse.ArgumentParser(description="Training and Infering Tic-Tac-Toe")
#parser.add_argument('--train', type=int, default=1, help='If 1, generate policies for 2 bots, else if 0 player play with bot #1')

if __name__ == "__main__":
    configs = Configs()
#    args = parser.parse_args()
    p1 = BotPlayer("computer")

#specific to bot------------------------
#    p1.exp_rate = 0.  # dont want to explore during competition
    p1.loadPolicy(os.path.join(configs.POLICIES_DIR, "policy_player_1"))

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    st.playGame()
