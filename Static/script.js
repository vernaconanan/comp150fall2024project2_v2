const gridContainer = document.getElementById('grid-container');
const gridSize = 4;
let cells = [];

const animalMap = {
    2: 'duck.jpg',
    4: 'monkey.jpg',
    8: 'koala.jpg',
    16: 'panda.jpg',
    32: 'fox.jpg',
    64: 'pig.jpg',
    128: 'lion.jpg',
    256: 'tiger.jpg',
    512: 'hippo.jpg',
    1024: 'elephant.jpg',
    2048: 'giraffe.jpg'
};

// Initialize grid
function createGrid() {
    gridContainer.innerHTML = '';
    cells = [];
    for (let i = 0; i < gridSize * gridSize; i++) {
        const cell = document.createElement('div');
        cell.classList.add('grid-cell');
        gridContainer.appendChild(cell);
        cells.push(cell);
    }
}

// Generate a new tile
function generateNewTile() {
    const emptyCells = cells.filter(cell => !cell.firstChild);
    if (emptyCells.length === 0) return;
    const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
    const tile = document.createElement('div');
    tile.classList.add('tile');
    tile.dataset.level = 2; // Starting value
    const img = document.createElement('img');
    img.src = `/static/${animalMap[2]}`;
    img.style.width = '80px';
    img.style.height = '80px';
    tile.appendChild(img);
    randomCell.appendChild(tile);
}

// Add event listener for keyboard input
document.addEventListener('keydown', handleKeyPress);

// Handle user input
function handleKeyPress(event) {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        // Logic for moving and merging tiles
        generateNewTile(); // Placeholder: Generate a new tile for now
    }
}

// Start the game
createGrid();
generateNewTile();
generateNewTile();
