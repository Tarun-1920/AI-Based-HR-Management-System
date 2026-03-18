const mongoose = require('mongoose');

const documentSchema = new mongoose.Schema({
  documentName: { type: String, required: true },
  originalName: { type: String, required: true },
  employeeId: { type: String, required: true, index: true },
  fileType: { type: String, required: true },
  documentType: { 
    type: String, 
    enum: ['resume', 'certificate', 'offer_letter', 'employee_report', 'other'],
    required: true 
  },
  fileSize: { type: Number, required: true },
  filePath: { type: String, required: true },
  s3Key: { type: String },
  uploadDate: { type: Date, default: Date.now },
  version: { type: Number, default: 1 },
  previousVersions: [{
    documentName: String,
    filePath: String,
    s3Key: String,
    version: Number,
    uploadDate: Date
  }],
  uploadedBy: { type: String, required: true },
  metadata: { type: Map, of: String }
}, { timestamps: true });

documentSchema.index({ employeeId: 1, documentType: 1 });

module.exports = mongoose.model('Document', documentSchema);
