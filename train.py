import pandas as pd
from environment import BusinessLogEnv
from q_learning_agent import QLearningAgent
from sarsa_agent import SarsaAgent
import numpy as np


data = pd.read_csv("/home/srinivasan/Skan/Models/BPM_RL/filtered_data_reduced.csv").head(10000)
# x - correct   2x - 10000    r + 10000 / 20000
# data = data[data['case_id']=="62ca1700177dda71feb36f7770f30e06/149"]
data = data.fillna("")
pred_vars = ['case_id', 'app_name_activity', 'unhashed_active_url']

k = 3
env = BusinessLogEnv(data, k, pred_vars)

action_size = len(env.action_space)
agent = SarsaAgent(action_size, learning_rate=0.1, discount_factor=0.99, epsilon=0.1, epsilon_decay=0.995, epsilon_min=0.01)

num_episodes = 20000

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.get_action(state)
        next_state, reward, done = env.step(action)
        agent.update_q_table(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
    
    if episode%100 == 0:
        print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

    # # Optionally, save the Q-table every few episodes
    # if (episode + 1) % 100 == 0:
    #     with open(f'q_table_{episode + 1}.npy', 'wb') as f:
    #         np.save(f, agent.q_table)
