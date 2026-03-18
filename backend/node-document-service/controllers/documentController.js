const Document = require('../models/Document');
const fs = require('fs').promises;
const path = require('path');

exports.uploadDocument = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { employeeId, documentType, uploadedBy } = req.body;
    
    if (!employeeId || !documentType || !uploadedBy) {
      await fs.unlink(req.file.path);
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Check for existing document to handle versioning
    const existingDoc = await Document.findOne({ 
      employeeId, 
      documentType,
      originalName: req.file.originalname 
    }).sort({ version: -1 });

    let newVersion = 1;
    let previousVersions = [];

    if (existingDoc) {
      newVersion = existingDoc.version + 1;
      previousVersions = [...existingDoc.previousVersions, {
        documentName: existingDoc.documentName,
        filePath: existingDoc.filePath,
        s3Key: existingDoc.s3Key,
        version: existingDoc.version,
        uploadDate: existingDoc.uploadDate
      }];
    }

    const document = new Document({
      documentName: req.file.filename,
      originalName: req.file.originalname,
      employeeId,
      fileType: path.extname(req.file.originalname).substring(1),
      documentType,
      fileSize: req.file.size,
      filePath: req.file.path,
      uploadedBy,
      version: newVersion,
      previousVersions
    });

    await document.save();

    res.status(201).json({ 
      message: 'Document uploaded successfully', 
      document 
    });
  } catch (error) {
    if (req.file) await fs.unlink(req.file.path).catch(() => {});
    res.status(500).json({ error: error.message });
  }
};

exports.getDocuments = async (req, res) => {
  try {
    const { employeeId, documentType } = req.query;
    const filter = {};
    
    if (employeeId) filter.employeeId = employeeId;
    if (documentType) filter.documentType = documentType;

    const documents = await Document.find(filter).sort({ uploadDate: -1 });
    res.json({ documents });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getDocumentById = async (req, res) => {
  try {
    const document = await Document.findById(req.params.id);
    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }
    res.json({ document });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.downloadDocument = async (req, res) => {
  try {
    const document = await Document.findById(req.params.id);
    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }

    res.download(document.filePath, document.originalName);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteDocument = async (req, res) => {
  try {
    const document = await Document.findById(req.params.id);
    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }

    // Delete file from storage
    await fs.unlink(document.filePath).catch(() => {});
    
    // Delete previous versions
    for (const version of document.previousVersions) {
      if (version.filePath) {
        await fs.unlink(version.filePath).catch(() => {});
      }
    }

    await Document.findByIdAndDelete(req.params.id);
    res.json({ message: 'Document deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getDocumentVersions = async (req, res) => {
  try {
    const document = await Document.findById(req.params.id);
    if (!document) {
      return res.status(404).json({ error: 'Document not found' });
    }

    const versions = [
      {
        version: document.version,
        uploadDate: document.uploadDate,
        fileSize: document.fileSize,
        current: true
      },
      ...document.previousVersions.map(v => ({
        version: v.version,
        uploadDate: v.uploadDate,
        current: false
      }))
    ];

    res.json({ versions });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
