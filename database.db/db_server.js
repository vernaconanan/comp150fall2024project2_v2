import express from 'express';
import mongoose from 'mongoose';
import bodyParser from 'body-parser';
import cors from 'cors';

// Database URL (change as needed)
const DB_URL = 'mongodb://localhost:27017/game_database';

// Connect to MongoDB
mongoose.connect(DB_URL, { useNewUrlParser: true, useUnifiedTopology: true });

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Define Schemas
const gameStateSchema = new mongoose.Schema({
    grid: [[Number]], // 2D array for the grid
    score: { type: Number, default: 0 },
    gameOver: { type: Boolean, default: false },
});

const bestScoreSchema = new mongoose.Schema({
    bestScore: { type: Number, default: 0 },
});

// Models
const GameState = mongoose.model('GameState', gameStateSchema);
const BestScore = mongoose.model('BestScore', bestScoreSchema);

// API Routes
// Get current game state
app.get('/state', async (req, res) => {
    try {
        const state = await GameState.findOne();
        const bestScore = await BestScore.findOne();
        res.json({ state, bestScore: bestScore?.bestScore || 0 });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Save game state
app.post('/state', async (req, res) => {
    try {
        const { grid, score, gameOver } = req.body;

        let state = await GameState.findOne();
        if (state) {
            state.grid = grid;
            state.score = score;
            state.gameOver = gameOver;
            await state.save();
        } else {
            state = new GameState({ grid, score, gameOver });
            await state.save();
        }

        res.json({ message: 'Game state saved', state });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Save best score
app.post('/best-score', async (req, res) => {
    try {
        const { bestScore } = req.body;

        let score = await BestScore.findOne();
        if (score) {
            score.bestScore = Math.max(score.bestScore, bestScore);
            await score.save();
        } else {
            score = new BestScore({ bestScore });
            await score.save();
        }

        res.json({ message: 'Best score saved', bestScore: score.bestScore });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Database server running on port ${PORT}`);
});
