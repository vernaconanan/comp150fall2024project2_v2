// Pre-existing functionality
const gridContainer = document.getElementById("game-board");
const gameOverOverlay = document.createElement("div");
gameOverOverlay.id = "game-over";

gameOverOverlay.innerHTML = `
    <p>Game Over!</p>
    <button id="close-game-over">Close</button>
    <button id="restart-from-gameover">Restart</button>
`;
document.body.appendChild(gameOverOverlay);

const restartButton = document.getElementById("restart-button");

// Audio elements (add these IDs in the HTML for sound files)
const mergeSound = document.getElementById('mergeSound');
const gameOverSound = document.getElementById('gameOverSound');
const newGameSound = document.getElementById('newGameSound');

// Render the grid
function renderGrid(grid) {
    gridContainer.innerHTML = "";
    grid.forEach(row => {
        row.forEach(cell => {
            const tile = document.createElement("div");
            tile.className = "grid-cell";

            // Check if the cell has a high value
            if (cell >= 128) {
                tile.classList.add("tile-high-value"); // Add glow effect for high-value tiles
            }

            if (cell !== 0) {
                const img = document.createElement("img");
                img.src = `/static/images/${animalMap[cell]}`;
                img.alt = `Animal for tile value ${cell}`;
                tile.appendChild(img);
            }

            gridContainer.appendChild(tile);
        });
    });
}

// Function to update the score display with animation
function updateScore(newScore) {
    const scoreElement = document.getElementById("score");

    // Temporarily add the 'score-updated' class to trigger animation
    scoreElement.classList.add("score-updated");

    // Set the new score
    scoreElement.innerText = newScore;

    // Remove the animation class after the animation duration
    setTimeout(() => {
        scoreElement.classList.remove("score-updated");
    }, 500); // Matches the duration of the animation (0.5s)
}

// Fetch current game state
async function fetchState() {
    const response = await fetch("/state");
    const data = await response.json();
    renderGrid(data.grid);
    document.getElementById("score").innerText = data.score;
    document.getElementById("best-score").innerText = data.best_score;

    // Ensure the game overlays are hidden on game start
    hideGameOver();
    hideGameWin();

    if (data.gameOver) {
        showGameOver();
        playGameOverSound();
    } else if (data.gameWon) {
        showGameWin();
    }
}

// Handle a move request
async function makeMove(direction) {
    const response = await fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction }),
    });

    if (response.ok) {
        const data = await response.json();
        renderGrid(data.grid);
        document.getElementById("score").innerText = data.score;
        document.getElementById("best-score").innerText = data.best_score;

        // Check if the game is over or won, and show the respective overlay
        if (data.gameOver) {
            showGameOver();
            playGameOverSound();
        } else if (data.gameWon) {
            showGameWin();
        } else {
            playMergeSound();
        }
    }
}

// Function to trigger the tile explosion animation
function explodeTiles() {
    const gridCells = document.querySelectorAll(".grid-cell");
    gridCells.forEach(cell => {
        // Apply the 'explode' class to each grid cell
        cell.classList.add("explode");

        // Remove the animation class after it finishes, so it can be reused
        cell.addEventListener("animationend", () => {
            cell.classList.remove("explode");
        });
    });
}

// Show game over screen with explosion effect
function showGameOver() {
    gameOverOverlay.style.display = "flex"; // Show the game over screen
    setTimeout(() => { // Delay explosion to ensure overlay shows first
        explodeTiles();  // Trigger the tile explosion animation when game is over
    }, 200); // You can adjust the timeout to control when the animation starts
}

// Hide game over screen
function hideGameOver() {
    gameOverOverlay.style.display = "none";
}

// Restart the game
async function restartGame() {
    const response = await fetch("/restart", { method: "POST" });
    if (response.ok) {
        hideGameOver();
        playNewGameSound();
        fetchState();  // Reset the game state when restarting
    }
}


// Event listeners for game over actions
document.getElementById("close-game-over").addEventListener("click", hideGameOver);
document.getElementById("restart-from-gameover").addEventListener("click", restartGame);
restartButton.addEventListener("click", restartGame);

// [Add the celebratory "You Win!" logic here]
const gameWinOverlay = document.createElement("div");
gameWinOverlay.id = "game-win";

gameWinOverlay.innerHTML = `
    <h1>You Win!</h1>
    <button id="close-game-win">Close</button>
    <button id="restart-from-win">Restart</button>
`;
document.body.appendChild(gameWinOverlay);

// Function to show the celebratory "You Win!" screen with animation
function showGameWin() {
    gameWinOverlay.style.display = "flex"; // Display the win overlay

    // Add confetti effect
    createConfetti();
}

// Function to create confetti
function createConfetti() {
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement("div");
        confetti.classList.add("confetti");
        confetti.style.left = `${Math.random() * 100}vw`; // Random horizontal position
        confetti.style.animationDuration = `${Math.random() * 2 + 2}s`; // Random duration for each confetti piece
        document.body.appendChild(confetti);

        // Remove confetti after animation ends to avoid clutter
        confetti.addEventListener("animationend", () => {
            confetti.remove();
        });
    }
}

// Hide the "You Win!" screen
function hideGameWin() {
    gameWinOverlay.style.display = "none";
}

// Restart the game from the win screen
async function restartGame() {
    const response = await fetch("/restart", { method: "POST" });
    if (response.ok) {
        hideGameWin();
        playNewGameSound();
        fetchState();  // Reset the game state when restarting
    }
}

// Event listeners for the "You Win!" screen actions
document.getElementById("close-game-win").addEventListener("click", hideGameWin);
document.getElementById("restart-from-win").addEventListener("click", restartGame);

// Keyboard event handling
document.addEventListener("keydown", (event) => {
    const keyMap = {
        ArrowUp: "UP",
        ArrowDown: "DOWN",
        ArrowLeft: "LEFT",
        ArrowRight: "RIGHT",
    };

    if (keyMap[event.key]) {
        event.preventDefault();
        makeMove(keyMap[event.key]);
    }
});

// Play sound for merge
function playMergeSound() {
    mergeSound.play();
}

// Play sound when the game is over
function playGameOverSound() {
    gameOverSound.play();
}

// Play sound when a new game starts
function playNewGameSound() {
    newGameSound.play();
}

// Initialize the game state on load
fetchState();
