const express = require('express');
const router = express.Router();
const upload = require('../middleware/upload');
const documentController = require('../controllers/documentController');

router.post('/upload', upload.single('document'), documentController.uploadDocument);
router.get('/', documentController.getDocuments);
router.get('/:id', documentController.getDocumentById);
router.get('/:id/download', documentController.downloadDocument);
router.delete('/:id', documentController.deleteDocument);
router.get('/:id/versions', documentController.getDocumentVersions);

module.exports = router;
