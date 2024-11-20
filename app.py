from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

GRID_SIZE = 4
animal_map = {
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
    2048: "giraffe.jpg",
}

# Global game state (for simplicity)
game_state = {
    "grid": [[0] * GRID_SIZE for _ in range(GRID_SIZE)],
    "score": 0,
}

def add_new_tile(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

@app.route("/")
def index():
    # Pass `animal_map` to the template
    return render_template("index.html", animal_map=animal_map)

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(game_state)

def merge_left(row):
    # Slide non-zero numbers to the left
    new_row = [num for num in row if num != 0]
    for i in range(len(new_row) - 1):
        # Merge tiles if they have the same value
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
            game_state["score"] += new_row[i]  # Update score
    # Remove zeros again after merging
    new_row = [num for num in new_row if num != 0]
    return new_row + [0] * (GRID_SIZE - len(new_row))


def move_left(grid):
    return [merge_left(row) for row in grid]


def move_right(grid):
    return [list(reversed(merge_left(reversed(row)))) for row in grid]


def move_up(grid):
    transposed = list(zip(*grid))  # Transpose the grid
    moved = move_left(transposed)  # Move left on transposed grid
    return [list(row) for row in zip(*moved)]  # Transpose back


def move_down(grid):
    transposed = list(zip(*grid))  # Transpose the grid
    moved = move_right(transposed)  # Move right on transposed grid
    return [list(row) for row in zip(*moved)]  # Transpose back


@app.route("/move", methods=["POST"])
def move():
    direction = request.json.get("direction")
    if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
        return jsonify({"error": "Invalid move"}), 400

    # Copy the current grid for comparison
    old_grid = [row[:] for row in game_state["grid"]]

    # Apply the move
    if direction == "UP":
        game_state["grid"] = move_up(game_state["grid"])
    elif direction == "DOWN":
        game_state["grid"] = move_down(game_state["grid"])
    elif direction == "LEFT":
        game_state["grid"] = move_left(game_state["grid"])
    elif direction == "RIGHT":
        game_state["grid"] = move_right(game_state["grid"])

    # Check if the grid changed (valid move)
    if game_state["grid"] != old_grid:
        add_new_tile(game_state["grid"])  # Add a new tile after a valid move

    return jsonify(game_state)


if __name__ == "__main__":
    # Initialize the game with two tiles
    add_new_tile(game_state["grid"])
    add_new_tile(game_state["grid"])
    app.run(debug=True)
