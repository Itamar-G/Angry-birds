from DQN import DQN
from ai_agent import DQN_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
import matplotlib.pyplot as plt
import numpy as np

import torch 
epochs = 10000
C = 500
batch = 64
learning_rate = 0.1
path = "Data/DQN_PARAM_Advanced_2.pth"

def train():
    state=State()
    env = Environment(state)
    env.init_display()
    player = DQN_Agent(env=env)
    replay = ReplayBuffer()
    Q = player.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.SGD(Q.parameters(), lr=learning_rate)
    success_rate = []

    for epoch in range(epochs):
        if epoch%C==0: success_rate.append(0) 
        env.reset()
        pigs=len(env.pigs)
        tries=env.tries
        print (epoch, end="\r")
        state=env.state
        while not env.end_of_game() and pigs>0 and tries>0:
            action = player.get_action(state, epoch=epoch)
            next_state, reward, done = env.move(action)
            while env.bird.move:
                next_state, reward, done = env.move(None)
                env.render()
            print(env.calculate_ballistic_distance(45,315,action,400,45))
            pigs=len(env.pigs)
            tries=env.tries
            if env.end_of_game():
                replay.push(env,state, action, reward, next_state, env.end_of_game())
                break
            replay.push(env, state, action, reward, next_state, env.end_of_game())
            state = next_state
            if epoch < 500:
                continue
            states, actions, rewards, next_states, dones = replay.sample(batch)
            Q_values = Q(states, actions)
            next_actions = player.get_actions(next_states, dones)
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states, next_actions)
            
            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
        if pigs == 0: success_rate[int(epoch/C)] += 1
        if epoch % C == 0 and epoch != 0:
            Q_hat.load_state_dict(Q.state_dict())
            print("epoch:", epoch, "wins:",success_rate[int(epoch/C-1)])
            
    player.save_param(path)
    plot_results(success_rate)
def plot_results(success_rate):
    plt.figure(figsize=(20, 500))
    plt.plot(success_rate, label='wins')
    plt.title('wins per 500 Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Number of Wins')
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    train()