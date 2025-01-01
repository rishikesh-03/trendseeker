const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const cors = require('cors');

const app = express();
const port = 3000;

// CORS configuration
// const corsOptions = {
//     origin: true, // Allow requests from any origin
//     methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
//     allowedHeaders: 'Content-Type, Authorization', // Add any other headers you need
//     preflightContinue: false,
//     optionsSuccessStatus: 204
// };


app.use(cors(corsOptions));
app.use(express.json());

// Handle preflight requests
app.options('*', cors(corsOptions));

// Endpoint to execute b.py
app.post('/run-script', (req, res) => {
    const { startDate, endDate } = req.body;

    if (!startDate || !endDate) {
        return res.status(400).json({ error: 'Please provide both startDate and endDate.' });
    }

    const command = `python "${path.join(__dirname, '../b.py')}" ${startDate} ${endDate}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing b.py: ${error.message}`);
            return res.status(500).json({ error: 'Error executing script.' });
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        try {
            const output = JSON.parse(stdout);
            res.json(output);
        } catch (parseError) {
            console.error(`Error parsing JSON output: ${parseError.message}`);
            res.status(500).json({ error: 'Error parsing script output.' });
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
