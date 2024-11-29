import random
import json
import os


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.ai_memory = self.load_ai_memory()
        self.last_move = None  # Initialiseer last_move

    def display_board(self):
        for i, row in enumerate(self.board):
            print("  " + " | ".join(row))
            if i < 2:
                print(" ---+---+---")

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def load_ai_memory(self):
        try:
            with open('ai_memory.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  # Als het bestand niet bestaat, begin met een leeg geheugen

    def save_ai_memory(self):
        with open('ai_memory.json', 'w') as f:
            json.dump(self.ai_memory, f, indent=4)  # Maak het overzichtelijk met `indent=4`

    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':  # Rows
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':  # Columns
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':  # Diagonal
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':  # Other diagonal
            return self.board[0][2]
        return None

    def is_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def get_empty_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def ai_choose_move(self):
        # Controleer eerst of de AI kan winnen in deze zet
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    # Voer de zet uit
                    self.board[row][col] = 'O'
                    if self.check_winner() == 'O':
                        return (row, col)
                    # Zet terug
                    self.board[row][col] = ' '

        # Controleer of de speler kan winnen en blokkeer die zet
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    # Voer de zet van de speler uit
                    self.board[row][col] = 'X'
                    if self.check_winner() == 'X':
                        # Blokkeer deze zet
                        self.board[row][col] = 'O'
                        return (row, col)
                    # Zet terug
                    self.board[row][col] = ' '

        # Anders, kies een willekeurige beschikbare zet
        available_moves = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
        if available_moves:
            return random.choice(available_moves)

        # Geen beschikbare zetten, dit zou niet moeten gebeuren
        return None

        # If no learned move, pick the best option based on heuristics
        for move in self.get_empty_cells():
            row, col = move
            self.board[row][col] = 'O'
            if self.check_winner() == 'O':
                self.board[row][col] = ' '
                return move
            self.board[row][col] = ' '

        for move in self.get_empty_cells():
            row, col = move
            self.board[row][col] = 'X'
            if self.check_winner() == 'X':
                self.board[row][col] = ' '
                return move
            self.board[row][col] = ' '

        return random.choice(self.get_empty_cells())

    def board_to_string(self):
        return ''.join(''.join(row) for row in self.board)

    def learn_from_game(self, winner):
        if winner == 'O':  # Alleen leren als de AI wint
            board_state = self.board_to_string()
            # Laad het huidige geheugen vanuit het bestand
            existing_memory = self.load_ai_memory()
            if board_state not in existing_memory:  # Voeg alleen toe als het nog niet bestaat
                existing_memory[board_state] = self.last_move
                self.ai_memory = existing_memory
                self.save_ai_memory()  # Sla de gecombineerde data op

    def play(self):
        print("Welkom bij Boter, Kaas en AI-eren!")
        while True:
            self.reset_board()
            self.display_board()
            winner = None

            while True:
                # Spelerbeurt
                try:
                    move = input("Voer uw zet in (rij kolom): ").strip()
                    row, col = map(int, move.split())
                    if not (1 <= row <= 3 and 1 <= col <= 3):
                        raise ValueError
                    if not self.make_move(row - 1, col - 1, 'X'):
                        print("Vakje is al bezet. Probeer opnieuw.")
                        continue
                except ValueError:
                    print("Ongeldige invoer. Voer een geldige rij en kolom in (bijv. 1 3).")
                    continue

                # Toon bord en controleer op winnaar
                self.display_board()
                winner = self.check_winner()
                if winner:
                    print(f"{winner} heeft gewonnen!")
                    break
                if self.is_draw():
                    print("Het is gelijkspel!")
                    break

                # AI-beurt
                ai_move = self.ai_choose_move()
                self.make_move(ai_move[0], ai_move[1], 'O')
                self.last_move = ai_move  # Update last_move met de huidige zet van de AI
                print(f"AI kiest: {ai_move[0] + 1} {ai_move[1] + 1}")

                # Toon bord en controleer op winnaar
                self.display_board()
                winner = self.check_winner()
                if winner:
                    print(f"{winner} heeft gewonnen!")
                    break
                if self.is_draw():
                    print("Het is gelijkspel!")
                    break

            # Laat de AI leren en sla geheugen op
            self.learn_from_game(winner)
            self.save_ai_memory()

            # Vraag of de speler opnieuw wil spelen
            replay = input("Wil je opnieuw spelen? (ja/nee): ").strip().lower()
            if replay != 'ja':
                print("Bedankt voor het spelen!")
                break


if __name__ == "__main__":
    game = TicTacToe()
    game.play()
