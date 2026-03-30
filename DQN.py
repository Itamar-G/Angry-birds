import math
import random
from typing import Any
import torch
import torch.nn as nn
import torch.nn.functional as F
from Environment import Environment
from State import *
import os
HuberLoss = nn.SmoothL1Loss()
env=Environment()
input_size = 1 + 2*max_pigs + 6*max_blocks # וודא ש-max_blocks מעודכן ל-2 לפחות
layer1 = 256  # הגדלה מ-128
layer2 = 256
layer3 = 128  # הוספת שכבה נוספת
output_size = 100
gamma = 0.99

class DQN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, output_size)
        )
        
    def forward(self, x):
        return self.net(x)
    
    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    import os   # אם אין למעלה בקובץ

    def save_params(self, path):
        dir_name = os.path.dirname(path)
        if dir_name != "":
            os.makedirs(dir_name, exist_ok=True)
        torch.save(self.state_dict(), path)

    def copy (self):
        new_DQN = DQN()
        new_DQN.load_state_dict(self.state_dict())
        return new_DQN
    
    def loss(self, Q_value, rewards, Q_next_Values, Dones):
        # חישוב ה-Target לפי משוואת בלמן
        Q_new = rewards + gamma * Q_next_Values * (1 - Dones)
        
        # שימוש ב-Huber Loss במקום MSE
        return HuberLoss(Q_value, Q_new)

    def __call__(self, states, actions=None):
        return self.forward(states)
