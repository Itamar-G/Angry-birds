import math
import random
import torch
import torch.nn as nn
import numpy as np
from DQN import DQN
from State import State


epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 1000

# epochs = 1000
# batch_size = 64
gamma = 0.99 
MSELoss = nn.MSELoss()
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

    def get_action (self, state: State, epoch = 0, events= None, train = True):
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actionsx = torch.arange(10)
        actionsy = torch.arange(10)
        if train and rnd < epsilon:
            return random.choice(actionsx),random.choice(actionsy)
        state_tensor = state.toTensor(self.env)
        xx, yy = torch.meshgrid(actionsx, actionsy, indexing="ij")
        action_pairs = torch.stack([xx.flatten(), yy.flatten()], dim=1)
        expand_state = state_tensor.unsqueeze(0).repeat(action_pairs.shape[0], 1)

        with torch.no_grad():
            Q_values = self.DQN(expand_state, action_pairs)
        # shape: [100]
        best_idx = torch.argmax(Q_values)
        best_action = action_pairs[best_idx]
        return int(best_action[0]), int(best_action[1])
    
    def get_actions (self, states, dones):
        actions = []
        for i, state in enumerate(states):
            actions.append(self.get_action(State.tensor_to_state_list(state), train=True)) #SARSA = True / Q-learning = False
        return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None, train=True, env=None):
        return self.get_action(state=state, train=train)
