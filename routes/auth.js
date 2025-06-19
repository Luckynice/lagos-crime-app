const express = require("express");
const jwt = require("jsonwebtoken");
const User = require("../models/User");
const router = express.Router();

// LOGIN
router.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (!user || !(await user.comparePassword(password))) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  const token = jwt.sign({ id: user._id, role: user.role }, process.env.JWT_SECRET, { expiresIn: "1d" });
  res.json({ token, user: { username: user.username, role: user.role } });
});

// REGISTER
router.post("/register", async (req, res) => {
  const { username, email, password, role } = req.body;
  try {
    const newUser = await User.create({ username, email, password, role });
    res.status(201).json({ message: "User created", user: { username: newUser.username, role: newUser.role } });
  } catch (err) {
    res.status(400).json({ message: "Registration failed", error: err.message });
  }
});

module.exports = router;
