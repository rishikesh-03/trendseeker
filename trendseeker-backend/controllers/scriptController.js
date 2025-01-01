// backend/controllers/scriptController.js
const { exec } = require('child_process');
const path = require('path');

exports.runScript = (req, res) => {
    const { startDate, endDate } = req.body;

    if (!startDate || !endDate) {
        return res.status(400).json({ error: 'Please provide both startDate and endDate.' });
    }

    const command = `python "${path.join(__dirname, '../b.py')}" ${startDate} ${endDate}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            // console.error(`Error executing b.py: ${error.message}`);
            return res.status(500).json({ error: 'Error executing script.' });
        }
        if (stderr) {
            // console.error(`stderr: ${stderr}`);
        }
        try {
            const output = JSON.parse(stdout);
            res.json(output);
        } catch (parseError) {
            // console.error(`Error parsing JSON output: ${parseError.message}`);
            res.status(500).json({ error: 'Error parsing script output.' });
        }
    });
};
