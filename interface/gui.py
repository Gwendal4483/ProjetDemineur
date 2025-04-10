import tkinter as tk
from game.board import Board

CELL_SIZE = 30  # Taille d’une cellule en pixels (optionnel si on ajuste avec width/height bouton)

class MinesweeperGUI:
    def __init__(self, root, width=10, height=10, mines=10):
        self.root = root
        self.board = Board(width, height, mines)
        self.buttons = {}

        # Conteneur principal
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Création des boutons pour chaque cellule
        for x in range(width):
            for y in range(height):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.on_left_click(x, y)
                )
                # Clic droit : drapeau
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                btn.grid(row=y, column=x)
                self.buttons[(x, y)] = btn

        # Zone de texte pour les messages ("gagné", "perdu", etc.)
        self.status = tk.Label(root, text="Bonne chance !")
        self.status.pack()

    def on_left_click(self, x, y):
        """Gère le clic gauche pour révéler une case"""
        cell = self.board.grid[x][y]
        if cell.is_flagged or cell.is_revealed:
            return

        self.board.reveal(x, y)

        if cell.is_mine:
            self.reveal_all()
            self.status.config(text="💥 Perdu !")
        elif self.board.has_won():
            self.reveal_all()
            self.status.config(text="🎉 Gagné !")

        self.update_ui()

    def on_right_click(self, x, y):
        """Gère le clic droit pour poser ou retirer un drapeau"""
        self.board.toggle_flag(x, y)
        self.update_ui()

    def update_ui(self):
        """Met à jour l’interface graphique pour refléter l’état du jeu"""
        for (x, y), btn in self.buttons.items():
            cell = self.board.grid[x][y]
            if cell.is_revealed:
                # Si la cellule est révélée, on affiche le nombre de mines voisines ou une mine
                btn.config(
                    relief=tk.SUNKEN,
                    text=str(cell.neighbor_mines) if not cell.is_mine else "*",
                    bg="white"
                )
            elif cell.is_flagged:
                # Cellule marquée comme drapeau
                btn.config(text="F", bg="lightyellow")
            else:
                # Cellule normale non révélée
                btn.config(text="", bg="SystemButtonFace")

    def reveal_all(self):
        """Révèle toutes les cellules (fin de partie)"""
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.board.grid[x][y].is_revealed = True

def launch_gui():
    """Fonction appelée pour lancer le jeu graphique"""
    root = tk.Tk()
    root.title("Démineur")
    MinesweeperGUI(root)
    root.mainloop()
