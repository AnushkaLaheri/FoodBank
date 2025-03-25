const express = require('express');
const app = express();
const authRoutes = require('./authRoutes');  // Import authRoutes

// Middleware to parse JSON data
app.use(express.json());

// Use authRoutes for authentication routes
app.use('/auth', authRoutes);  // All authentication routes will now start with /auth

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
