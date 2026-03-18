const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const documentRoutes = require('./routes/documentRoutes');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/hr_management', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('MongoDB connected'))
.catch(err => console.error('MongoDB connection error:', err));

// Routes
app.use('/api/documents', documentRoutes);

app.get('/health', (req, res) => {
  res.json({ status: 'OK', service: 'Document Management Service' });
});

const PORT = process.env.DOC_SERVICE_PORT || 5001;
app.listen(PORT, () => {
  console.log(`Document Management Service running on port ${PORT}`);
});

module.exports = app;
