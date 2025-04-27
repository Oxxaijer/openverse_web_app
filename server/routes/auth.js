const express = require('express');
const router = express.Router();

// Dummy registration route
router.post('/register', (req, res) => {
  res.status(400).json({ message: 'Registration validation failed.' });
});

// Dummy login route
router.post('/login', (req, res) => {
  res.status(401).json({ message: 'Login failed.' });
});

module.exports = router;
