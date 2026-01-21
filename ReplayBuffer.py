from collections import deque
import random
import torch
import numpy as np
from State import State


class ReplayBuffer:
    def __init__(self, capacity= 10000) -> None:
        self.buffer = deque(maxlen=capacity)

    def push (self, state : State, action, reward, next_state : State, done):
        self.buffer.append((state.toTensor(), torch.from_numpy(np.array(action)), 
                            torch.tensor(reward), next_state.toTensor(), torch.tensor(done)))

    def push_tensors (self, state_tensor, action_tensor, reward_tensor, next_state_tensor, done):
        self.buffer.append((state_tensor, action_tensor, reward_tensor, next_state_tensor, done))
            
    def sample (self, batch_size):
        if (batch_size > self.__len__()):
            batch_size = self.__len__()
        state_tensors, action_tensor, reward_tensors, \
                   next_state_tensors, dones = zip(*random.sample(self.buffer, batch_size))
        states = torch.vstack(state_tensors)
        actions = torch.vstack(action_tensor)
        rewards = torch.vstack(reward_tensors)
        next_states = torch.vstack(next_state_tensors)
        done_tensor = torch.tensor(dones).long().reshape(-1,1)
        return states, actions, rewards, next_states, done_tensor

    def __len__(self):
        return len(self.buffer)