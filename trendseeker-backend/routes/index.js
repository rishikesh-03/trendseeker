// backend/routes/index.js
const express = require('express');
const router = express.Router();
const scriptController = require('../controllers/scriptController');

// Endpoint to execute b.py
router.post('/run-script', scriptController.runScript);

module.exports = router;
