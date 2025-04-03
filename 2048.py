import tkinter as tk
import random

GRID_SIZE = 4
TILE_COLORS = {
    0: "#D6CCC2", 2: "#FAEDCD", 4: "#F7E1AE", 8: "#E9C46A",
    16: "#F4A261", 32: "#E76F51", 64: "#D67B52", 128: "#B08968",
    256: "#9C6644", 512: "#8B5E34", 1024: "#7F5539", 2048: "#6D4C41"

}

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry("400x500")
        self.root.configure(bg="#BBADA0")

        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.high_score = 0

        self.create_ui()
        self.spawn_tile()
        self.spawn_tile()
        self.update_grid()

        self.root.bind("<KeyPress>", self.handle_keypress)

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg="#BBADA0")
        self.frame.pack(pady=20)

        self.tiles = [[tk.Label(self.frame, text="", font=("Arial", 20, "bold"), width=4, height=2, bg="#CDC1B4", 
                                relief="raised", bd=5)
                       for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.tiles[row][col].grid(row=row, column=col, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14, "bold"), 
                                    bg="#BBADA0", fg="white")
        self.score_label.pack()

        self.high_score_label = tk.Label(self.root, text=f"High Score: {self.high_score}", font=("Arial", 14, "bold"), 
                                         bg="#BBADA0", fg="gold")
        self.high_score_label.pack()

    def update_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.grid[row][col]
                self.tiles[row][col].config(text=str(value) if value else "", bg=TILE_COLORS[value])

        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def move_tiles(self, direction):
        def compress(row):
            new_row = [val for val in row if val != 0]
            new_row += [0] * (GRID_SIZE - len(new_row))
            return new_row

        def merge(row):
            for i in range(GRID_SIZE - 1):
                if row[i] == row[i + 1] and row[i] != 0:
                    row[i] *= 2
                    self.score += row[i]
                    row[i + 1] = 0
            return row

        moved = False
        for i in range(GRID_SIZE):
            if direction in ("Up", "Down"):
                line = [self.grid[r][i] for r in range(GRID_SIZE)]
                if direction == "Down":
                    line.reverse()

                new_line = compress(line)
                new_line = merge(new_line)
                new_line = compress(new_line)

                if direction == "Down":
                    new_line.reverse()

                if [self.grid[r][i] for r in range(GRID_SIZE)] != new_line:
                    moved = True
                    for r in range(GRID_SIZE):
                        self.grid[r][i] = new_line[r]

            else:  # Left or Right
                line = self.grid[i][:]
                if direction == "Right":
                    line.reverse()

                new_line = compress(line)
                new_line = merge(new_line)
                new_line = compress(new_line)

                if direction == "Right":
                    new_line.reverse()

                if self.grid[i] != new_line:
                    moved = True
                    self.grid[i] = new_line

        if moved:
            self.spawn_tile()
            self.update_grid()
            if self.score > self.high_score:
                self.high_score = self.score
            if self.check_game_over():
                self.show_game_over()

    def handle_keypress(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.move_tiles(event.keysym)

    def check_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        for c in range(GRID_SIZE):
            for r in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def show_game_over(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("300x150")
        popup.configure(bg="#BBADA0")

        label = tk.Label(popup, text="Game Over!", font=("Arial", 20, "bold"), bg="#BBADA0", fg="white")
        label.pack(pady=20)

        restart_button = tk.Button(popup, text="Restart", font=("Arial", 14), bg="green", fg="white", command=self.restart_game)
        restart_button.pack()

    def restart_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()
        self.update_grid()

if __name__ == "__main__":
    root = tk.Tk()
    Game2048(root)
    root.mainloop()
