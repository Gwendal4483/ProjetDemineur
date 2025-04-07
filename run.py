from game.board import Board

def main():
    width, height, mines = 10, 10, 10
    board = Board(width, height, mines)

    print("Bienvenue dans le démineur (mode console) !")
    print("Commandes : r x y (révéler) | f x y (drapeau) | q (quitter)\n")

    while True:
        board.print_board()
        cmd = input("\n> ").strip().lower()

        if cmd == 'q':
            print("Au revoir !")
            break

        parts = cmd.split()
        if len(parts) != 3:
            print("Commande invalide. Exemple : r 3 4")
            continue

        action, x_str, y_str = parts
        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            print("Coordonnées invalides.")
            continue

        if not (0 <= x < width and 0 <= y < height):
            print("Coordonnées hors limites.")
            continue

        if action == 'r':
            board.reveal(x, y)
            if board.grid[x][y].is_mine:
                board.print_board(reveal_mines=True)
                print("\n💥 Boom ! Tu as perdu.")
                break
        elif action == 'f':
            board.toggle_flag(x, y)
        else:
            print("Action inconnue. Utilise 'r' ou 'f'.")

if __name__ == "__main__":
    main()
