from ai.env import MinesweeperEnv
from ai.agent import DQNAgent

import numpy as np
import matplotlib.pyplot as plt

# Hyperparamètres
GRID_SIZE = 5
N_MINES = 3
EPISODES = 3000
EPSILON_START = 1.0
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.995
LOG_INTERVAL = 100

# Environnement & Agent
env = MinesweeperEnv(width=GRID_SIZE, height=GRID_SIZE, n_mines=N_MINES)
agent = DQNAgent(width=GRID_SIZE, height=GRID_SIZE)

epsilon = EPSILON_START
all_rewards = []

for episode in range(1, EPISODES + 1):
    obs = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.act(obs, epsilon)
        next_obs, reward, done, _ = env.step(action)
        agent.remember(obs, action, reward, next_obs, done)
        agent.train()
        obs = next_obs
        total_reward += reward

    all_rewards.append(total_reward)

    # Décroissance de epsilon (exploration → exploitation)
    epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

    # Affichage tous les LOG_INTERVAL épisodes
    if episode % LOG_INTERVAL == 0:
        avg_reward = np.mean(all_rewards[-LOG_INTERVAL:])
        print(f"Épisode {episode} | Moy. reward: {avg_reward:.3f} | ε = {epsilon:.3f}")

# 🎨 Affichage final du score moyen par tranche
plt.plot(np.convolve(all_rewards, np.ones(LOG_INTERVAL) / LOG_INTERVAL, mode="valid"))
plt.title("Récompense moyenne (smoothing)")
plt.xlabel("Épisode")
plt.ylabel("Récompense moyenne")
plt.grid()
plt.show()
