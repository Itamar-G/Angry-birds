from DQN import DQN
from ai_agent import DQN_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State

import torch 
epochs = 50000
C = 300
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
            if epoch < 5000:
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
        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
            print("epoch:", epoch, "pigs:",pigs,"tries:",tries)

    player.save_param(path)
if __name__ == "__main__":
    train()