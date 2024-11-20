import random
import os
from PIL import Image, ImageTk
import tkinter as tk
from flask import Flask, jsonify, request

# Flask application setup
app = Flask(__name__)

# Global constants
IMAGE_SIZE = 100  # Size of each image tile
GRID_SIZE = 4  # 4x4 grid size

# Mapping of numbers to animal image filenames
animal_map = {
    0: None,  # Empty space
    2: "duck.jpg",
    4: "monkey.jpg",
    8: "koala.jpg",
    16: "panda.jpg",
    32: "fox.jpg",
    64: "pig.jpg",
    128: "lion.jpg",
    256: "tiger.jpg",
    512: "hippo.jpg",
    1024: "elephant.jpg",
    2048: "giraffe.jpg"
}

class AnimalTileGame:
    def __init__(self, canvas, image_dict):
        self.grid = self.initialize_game()
        self.canvas = canvas
        self.image_dict = image_dict
        self.display_grid()

    def initialize_game(self):
        grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile(grid)
        self.add_new_tile(grid)
        return grid

    def add_new_tile(self, grid):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            grid[r][c] = 2 if random.random() < 0.9 else 4

    def display_grid(self):
        self.canvas.delete("all")  # Clear previous images

        # Display the background image (already loaded)
        self.canvas.create_image(0, 0, anchor="nw", image=background_image)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                if value in animal_map and animal_map[value]:
                    image = self.image_dict.get(animal_map[value])
                    if image:
                        self.canvas.create_image(c * IMAGE_SIZE, r * IMAGE_SIZE, anchor="nw", image=image)
        self.canvas.update()

    def move(self, direction):
        moved = False
        if direction == "UP":
            self.grid = move_up(self.grid)
            moved = True
        elif direction == "LEFT":
            self.grid = move_left(self.grid)
            moved = True
        elif direction == "DOWN":
            self.grid = move_down(self.grid)
            moved = True
        elif direction == "RIGHT":
            self.grid = move_right(self.grid)
            moved = True

        if moved:
            self.add_new_tile(self.grid)
            self.display_grid()
            if is_game_over(self.grid):
                self.canvas.create_text(GRID_SIZE * IMAGE_SIZE / 2, GRID_SIZE * IMAGE_SIZE / 2, 
                                        text="Game Over!", font=("Arial", 24), fill="red")

def move_left(grid):
    return [merge_left(row) for row in grid]

def move_right(grid):
    return [list(reversed(merge_left(reversed(row)))) for row in grid]

def move_up(grid):
    return [list(row) for row in zip(*move_left(zip(*grid)))]

def move_down(grid):
    return [list(row) for row in zip(*move_right(zip(*grid)))]

def merge_left(row):
    new_row = [num for num in row if num != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [num for num in new_row if num != 0]
    return new_row + [0] * (GRID_SIZE - len(new_row))

def is_game_over(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                return False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r > 0 and grid[r][c] == grid[r - 1][c]) or \
               (r < GRID_SIZE - 1 and grid[r][c] == grid[r + 1][c]) or \
               (c > 0 and grid[r][c] == grid[r][c - 1]) or \
               (c < GRID_SIZE - 1 and grid[r][c] == grid[r][c + 1]):
                return False
    return True

def main():
    global background_image  # Make it a global variable to be used inside the class

    root = tk.Tk()
    root.title("Animal Tile Game")
    canvas = tk.Canvas(root, width=GRID_SIZE * IMAGE_SIZE, height=GRID_SIZE * IMAGE_SIZE)
    canvas.pack()

    # Load the background image
    background_image_path = os.path.join("static", "2048 setup.jpg")  # Make sure this path is correct
    try:
        bg_img = Image.open(background_image_path).resize((GRID_SIZE * IMAGE_SIZE, GRID_SIZE * IMAGE_SIZE), Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(bg_img)
    except FileNotFoundError:
        print(f"Warning: Background image not found at {background_image_path}.")
        background_image = None

    # Load animal images into a dictionary
    image_dict = {}
    for value, filename in animal_map.items():
        if filename:
            image_path = os.path.join("static", filename)
            try:
                img = Image.open(image_path).resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
                image_dict[filename] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print(f"Warning: Image '{filename}' not found at {image_path}.")
                image_dict[filename] = None

    game = AnimalTileGame(canvas, image_dict)

    def handle_key(event):
        if event.keysym in ['Up', 'W']:
            game.move("UP")
        elif event.keysym in ['Left', 'A']:
            game.move("LEFT")
        elif event.keysym in ['Down', 'S']:
            game.move("DOWN")
        elif event.keysym in ['Right', 'D']:
            game.move("RIGHT")

    root.bind("<Key>", handle_key)

    # Start Flask server in a separate thread if needed
    import threading
    threading.Thread(target=lambda: app.run(port=5000, debug=True, use_reloader=False)).start()

    root.mainloop()

if __name__ == "__main__":
    main()
