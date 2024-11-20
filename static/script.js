const gridContainer = document.getElementById("game-board");

function renderGrid(grid) {
    gridContainer.innerHTML = ""; // Clear previous grid
    grid.forEach(row => {
        row.forEach(cell => {
            const tile = document.createElement("div");
            tile.className = "grid-cell";
            if (cell !== 0) {
                const img = document.createElement("img");
                img.src = `/static/images/${animalMap[cell]}`; // animalMap comes from the backend
                img.alt = `Animal for tile value ${cell}`;
                tile.appendChild(img);
            }
            gridContainer.appendChild(tile);
        });
    });
}

async function fetchState() {
    const response = await fetch("/state");
    const data = await response.json();
    renderGrid(data.grid);
    document.getElementById("score").innerText = data.score;
}

async function makeMove(direction) {
    const response = await fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction }),
    });

    if (response.ok) {
        const data = await response.json();
        renderGrid(data.grid); // Update grid visuals
        document.getElementById("score").innerText = data.score; // Update score
    } else {
        console.error("Invalid move");
    }
}


document.addEventListener("keydown", (event) => {
    const keyMap = {
        ArrowUp: "UP",
        ArrowDown: "DOWN",
        ArrowLeft: "LEFT",
        ArrowRight: "RIGHT",
    };
    if (keyMap[event.key]) {
        makeMove(keyMap[event.key]);
    }
});

// Initial load
fetchState();
