from DQN import DQN
from ai_agent import DQN_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
import matplotlib.pyplot as plt
import numpy as np

import torch 
epochs = 10000
C = 1
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
    tries_history = []

    for epoch in range(epochs):
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
        tries_history.append(env.tries)
        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
            print("epoch:", epoch, "pigs:",pigs,"tries:",tries)
    player.save_param(path)
    plot_results(tries_history)
def plot_results(tries_history):
    plt.figure(figsize=(10, 5))
    plt.plot(tries_history, label='Remaining Tries')
    # הוספת ממוצע נע כדי לראות מגמת שיפור (אופציונלי)
    if len(tries_history) > 100:
        moving_avg = np.convolve(tries_history, np.ones(100)/100, mode='valid')
        plt.plot(range(99, len(tries_history)), moving_avg, label='Moving Average (100)', color='red')
    
    plt.title('Remaining Tries per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Tries Left')
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    train()