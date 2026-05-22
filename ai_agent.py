import math
import random
import torch
import torch.nn as nn
import numpy as np
from DQN import DQN
from State import State


epsilon_start = 1
epsilon_final = 0.01

gamma = 0.99 
class DQN_Agent:
    def __init__(self, parametes_path = None, train = True, env= None) -> None:
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train(train)
        self.env = env

    def train (self, train):
          self.train = train
          if train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self, state_T, epoch = 0, events= None, train = True):
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actionsx = torch.arange(10)
        actionsy = torch.arange(10)
        if train and rnd < epsilon:
            return random.choice(actionsx),random.choice(actionsy)
       
        with torch.no_grad():
            Q_values = self.DQN(state_T)
        # shape: [100]
        best_idx = torch.argmax(Q_values)
        best_action = self.index_to_action(best_idx)
        return best_action
    
    def index_to_action(self, index):
        x = index // 10
        y = index % 10
        return x, y

    def action_to_index(self, action):
        return action[0] * 10 + action[1]

    def get_actions (self, states, dones, train = True):
        actions = []
        for state in enumerate(states):
            actions.append(self.get_action(state, train=train)) #SARSA = True / Q-learning = False
        return torch.tensor(actions)

    def epsilon_greedy(self, epoch, total_epochs=1000000):
        start = 1.0
        final = 0.01
        decay_duration = total_epochs * 0.5
        epsilon = max(final, start - (start - final) * (epoch / decay_duration))
        return epsilon
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None, train=True, env=None):
        return self.get_action(state=state, train=train)
