const express = require('express');
const router = express.Router();

// Dummy search history route
router.get('/', (req, res) => {
  res.json({ message: 'Search history retrieved.' });
});

module.exports = router;
