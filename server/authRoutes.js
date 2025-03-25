const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const router = express.Router();

// Dummy user data for demo purposes
const users = [];

// JWT secret key
const SECRET_KEY = 'your_secret_key_here';  // Replace this with a strong secret key

// Route for user registration
router.post('/register', async (req, res) => {
  const { username, password } = req.body;
  
  // Check if the user already exists
  const userExists = users.find(user => user.username === username);
  if (userExists) {
    return res.status(400).send('User already exists');
  }

  // Hash the password
  const hashedPassword = await bcrypt.hash(password, 10); 

  // Save user data (in-memory for now)
  users.push({ username, password: hashedPassword }); 

  res.status(201).send('User registered successfully');
});

// Route for user login
router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  // Find user by username
  const user = users.find(user => user.username === username);
  if (!user) {
    return res.status(400).send('User not found');
  }

  // Compare entered password with hashed password
  const isPasswordValid = await bcrypt.compare(password, user.password);
  if (!isPasswordValid) {
    return res.status(400).send('Invalid password');
  }

  // Generate JWT token
  const token = jwt.sign({ username: user.username }, SECRET_KEY, { expiresIn: '1h' });

  res.json({ token });
});

module.exports = router;
