from DQN import DQN
from ai_agent import DQN_Agent
from Environment import Environment
from ReplayBuffer import ReplayBuffer
from State import State
import matplotlib.pyplot as plt
import numpy as np

import torch 
epochs = 50000
C = 2000
batch = 128
learning_rate = 0.0001
path = "Data/DQN_PARAM_Advanced_2.pth"

def train():
    state = State()
    env = Environment(state)
    env.init_display()
    player = DQN_Agent(env=env)
    replay = ReplayBuffer()
    Q = player.DQN
    Q_hat: DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.Adam(Q.parameters(), lr=0.0001)
    
    success_rate = []
    # --- הוספה: רשימות למעקב אחר loss ---
    loss_history = []
    current_epoch_losses = [] 
    # -----------------------------------

    for epoch in range(epochs):
        if epoch % C == 0: 
            success_rate.append(0)
        
        env.reset()
        pigs = len(env.pigs)
        tries = env.tries
        print(epoch, end="\r")
        state = env.state
        
        while not env.end_of_game() and pigs > 0 and tries > 0:
            action = player.get_action(state, epoch=epoch)
            next_state, reward, done = env.move(action)
            
            while env.bird.move:
                next_state, reward, done = env.move(None)
            
            pigs = len(env.pigs)
            tries = env.tries
            
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
            
            # --- הוספה: שמירת ערך ה-loss הנוכחי ---
            current_epoch_losses.append(loss.item())
            # ------------------------------------
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(Q.parameters(), max_norm=1.0)
            optim.step()
            optim.zero_grad()

        if pigs == 0: 
            success_rate[int(epoch/C)] += 1
            
        if epoch % C == 0 and epoch != 0:
            Q_hat.load_state_dict(Q.state_dict())
            
            # --- הוספה: חישוב ממוצע ה-loss לבלוק של 500/1000 איטרציות ---
            if current_epoch_losses:
                avg_loss = sum(current_epoch_losses) / len(current_epoch_losses)
                loss_history.append(avg_loss)
                current_epoch_losses = [] # איפוס לרשימה הבאה
            else:
                loss_history.append(0)
            
            print("epoch:", epoch, "wins:", success_rate[int(epoch/C-1)], "avg loss:", loss_history[-1])
            
    player.save_param(path)
    # עדכון הקריאה לפונקציית הציור
    plot_results(success_rate, loss_history)

# --- עדכון פונקציית הגרפים ---
def plot_results(success_rate, loss_history):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # גרף ניצחונות
    ax1.plot(success_rate, color='green', label='Wins')
    ax1.set_title('Wins per Interval')
    ax1.set_xlabel(f'Intervals (per {C} epochs)')
    ax1.set_ylabel('Number of Wins')
    ax1.grid(True)
    ax1.legend()

    # גרף Loss
    ax2.plot(loss_history, color='red', label='Loss')
    ax2.set_title('Average Loss per Interval')
    ax2.set_xlabel(f'Intervals (per {C} epochs)')
    ax2.set_ylabel('Loss Value')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    train()