import numpy as np
import pickle
import argparse
import os

from state import State
from player import BotPlayer
from configs import Configs

if __name__ == "__main__":
    configs = Configs()

    # play/train between bots

    p1 = BotPlayer("player_1")
    p2 = BotPlayer("player_2")

    st = State(p1, p2)
    st.playGame(configs.training_epoch)
