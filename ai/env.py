import gym 
import numpy as np 
from gym import spaces 
from game.board import Board

class MinesweeperEnv(gym.Env):

    def __init__(self, width=5, height=5, n_mines=5):
        super().__init__()
        self.width = width
        self.height = height
        self.n_mines = n_mines

        # Actions : une action correspond à (x, y, type)
        # - type = 0 → révéler une case
        # - type = 1 → poser/enlever un drapeau
        self.action_space = spaces.MultiDiscrete([self.width, self.height, 2])

        # Observation : grille visible, avec 3 canaux :
        #  - canal 0 : 1 si la case est révélée, 0 sinon
        #  - canal 1 : nombre de mines voisines (0 à 8), normalisé
        #  - canal 2 : 1 si drapeau, 0 sinon
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.width, self.height, 3),
            dtype=np.float32
        )

        self.board = None

    def reset(self):
        """Commence une nouvelle partie"""
        self.board = Board(self.width, self.height, self.n_mines)
        obs = self._get_observation()
        return obs

    def step(self, action):
        """
        Exécute une action de l'agent
        action = (x, y, type) → type=0 (click) ou type=1 (flag)
        """
        x, y, action_type = action
        done = False
        reward = 0

        cell = self.board.grid[x][y]

        if action_type == 0:  # Révéler
            if not cell.is_revealed and not cell.is_flagged:
                self.board.reveal(x, y)
                if cell.is_mine:
                    reward = -1.0
                    done = True
                else:
                    reward = 0.1
        elif action_type == 1:  # Drapeau
            self.board.toggle_flag(x, y)
            reward = 0.05  # petite récompense pour poser un drapeau (optionnel)

        if self.board.has_won():
            reward = 1.0
            done = True

        obs = self._get_observation()
        return obs, reward, done, {}

    def _get_observation(self):
        """Retourne la grille visible sous forme de tenseur normalisé"""
        obs = np.zeros((self.width, self.height, 3), dtype=np.float32)

        for x in range(self.width):
            for y in range(self.height):
                cell = self.board.grid[x][y]
                if cell.is_revealed:
                    obs[x, y, 0] = 1.0  # révélée
                    obs[x, y, 1] = cell.neighbor_mines / 8.0  # normalisé
                if cell.is_flagged:
                    obs[x, y, 2] = 1.0

        return obs

    def render(self, mode='human'):
        """Affiche la grille dans le terminal"""
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                cell = self.board.grid[x][y]
                if cell.is_flagged:
                    row += 'F '
                elif not cell.is_revealed:
                    row += '. '
                elif cell.is_mine:
                    row += '* '
                else:
                    row += str(cell.neighbor_mines) + ' '
            print(row)
        print()

    def close(self):
        pass
