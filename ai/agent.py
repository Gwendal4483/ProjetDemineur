import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# Réseau de neurones simple pour approximer les Q-values
class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self, width, height, n_actions=2, gamma=0.99, lr=1e-3, batch_size=64):
        self.width = width
        self.height = height
        self.input_dim = width * height * 3  # 3 canaux (révélé, voisinage, drapeau)
        self.output_dim = width * height * n_actions  # 2 actions possibles par case

        self.gamma = gamma
        self.batch_size = batch_size
        self.lr = lr

        self.model = QNetwork(self.input_dim, self.output_dim)
        self.target_model = QNetwork(self.input_dim, self.output_dim)
        self.target_model.load_state_dict(self.model.state_dict())

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.target_model.to(self.device)

        self.memory = deque(maxlen=100_000)
        self.steps = 0
        self.update_target_every = 1000  # fréquence de mise à jour du modèle cible

    def act(self, state, epsilon=0.1):
        """
        Stratégie ε-greedy : exploration aléatoire ou exploitation
        """
        if random.random() < epsilon:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            action_type = random.randint(0, 1)
            return (x, y, action_type)

        # Exploitation : choisir l'action avec la Q-value maximale
        state_tensor = torch.FloatTensor(state).view(1, -1).to(self.device)
        with torch.no_grad():
            q_values = self.model(state_tensor).cpu().numpy().squeeze()

        best_index = np.argmax(q_values)
        cell_idx, action_type = divmod(best_index, 2)
        x, y = divmod(cell_idx, self.height)
        return (x, y, action_type)

    def remember(self, state, action, reward, next_state, done):
        """
        Stocke une transition dans le buffer de replay
        """
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        """
        Apprentissage sur un batch de transitions
        """
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states_tensor = torch.FloatTensor(states).view(self.batch_size, -1).to(self.device)
        next_states_tensor = torch.FloatTensor(next_states).view(self.batch_size, -1).to(self.device)

        q_values = self.model(states_tensor)
        next_q_values = self.target_model(next_states_tensor).detach()

        # Calcul des cibles
        target_q = q_values.clone()
        for i, (action, reward, done) in enumerate(zip(actions, rewards, dones)):
            x, y, action_type = action
            index = (x * self.height + y) * 2 + action_type  # conversion (x, y, type) → index
            if done:
                target = reward
            else:
                target = reward + self.gamma * torch.max(next_q_values[i])
            target_q[i, index] = target

        # Optimisation
        loss = self.loss_fn(q_values, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps += 1
        if self.steps % self.update_target_every == 0:
            self.target_model.load_state_dict(self.model.state_dict())
