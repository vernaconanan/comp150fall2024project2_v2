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

    # Global game state
game_state = {
        "grid": [[0] * GRID_SIZE for _ in range(GRID_SIZE)],  # Empty grid
        "score": 0,
        "gameOver": False,  # Start with no Game Over
    }

    # Track the best score
best_score = 0


def add_new_tile(grid):
        """Add a new tile (2 or 4) to a random empty cell."""
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            grid[r][c] = 2 if random.random() < 0.9 else 4


def is_game_over(grid):
        """Check if no moves are possible."""
        for row in grid:
            if 0 in row:  # Empty cell exists
                return False
        for row in grid:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:  # Merge possible horizontally
                    return False
        for col in range(len(grid[0])):
            for row in range(len(grid) - 1):
                if grid[row][col] == grid[row + 1][col]:  # Merge possible vertically
                    return False
        return True


@app.route("/")
def index():
        return render_template("index.html", animal_map=animal_map)


@app.route("/state", methods=["GET"])
def get_state():
        """Return the current game state."""
        return jsonify({
            "grid": game_state["grid"],
            "score": game_state["score"],
            "best_score": best_score,
            "gameOver": game_state["gameOver"]
        })


@app.route("/move", methods=["POST"])
def move():
        """Handle a move request."""
        global best_score
        direction = request.json["direction"] if request.json and "direction" in request.json else None
        if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
            return jsonify({"error": "Invalid move"}), 400

        old_grid = [row[:] for row in game_state["grid"]]

        if direction == "UP":
            game_state["grid"] = move_up(game_state["grid"])
        elif direction == "DOWN":
            game_state["grid"] = move_down(game_state["grid"])
        elif direction == "LEFT":
            game_state["grid"] = move_left(game_state["grid"])
        elif direction == "RIGHT":
            game_state["grid"] = move_right(game_state["grid"])

        if game_state["grid"] != old_grid:  # Valid move
            add_new_tile(game_state["grid"])

        # Update game over state
        game_state["gameOver"] = is_game_over(game_state["grid"])

        # Update the best score
        if game_state["score"] > best_score:
            best_score = game_state["score"]

        return jsonify({
            "grid": game_state["grid"],
            "score": game_state["score"],
            "best_score": best_score,
            "gameOver": game_state["gameOver"]
        })


@app.route("/restart", methods=["POST"])
def restart():
        """Restart the game."""
        global game_state
        game_state = {
            "grid": [[0] * GRID_SIZE for _ in range(GRID_SIZE)],
            "score": 0,
            "gameOver": False,
        }
        add_new_tile(game_state["grid"])
        add_new_tile(game_state["grid"])
        return jsonify({
            "grid": game_state["grid"],
            "score": game_state["score"],
            "best_score": best_score,
            "gameOver": game_state["gameOver"]
        })


def move_left(grid):
        return [merge_left(row) for row in grid]


def move_right(grid):
        return [list(reversed(merge_left(reversed(row)))) for row in grid]


def move_up(grid):
        transposed = list(zip(*grid))
        moved = move_left(transposed)
        return [list(row) for row in zip(*moved)]


def move_down(grid):
        transposed = list(zip(*grid))
        moved = move_right(transposed)
        return [list(row) for row in zip(*moved)]


def merge_left(row):
        """Slide and merge a single row to the left."""
        new_row = [num for num in row if num != 0]  # Remove zeros
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:  # Merge adjacent tiles
                new_row[i] *= 2
                new_row[i + 1] = 0
                game_state["score"] += new_row[i]
        new_row = [num for num in new_row if num != 0]  # Remove zeros again
        return new_row + [0] * (GRID_SIZE - len(new_row))  # Fill with zeros


if __name__ == "__main__":
        # Initialize game with two tiles
        add_new_tile(game_state["grid"])
        add_new_tile(game_state["grid"])
        app.run(debug=True)