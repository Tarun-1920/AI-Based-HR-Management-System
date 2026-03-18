# Document Management Module - HR Management System

A complete document management solution with file upload, version control, and secure storage.

## Features

✅ **Upload Documents**: Resume, Certificates, Offer Letters, Employee Reports
✅ **Secure Storage**: Local storage (default) or AWS S3
✅ **Document Management**: View, Download, Delete documents
✅ **Version Control**: Automatic versioning for document updates
✅ **Metadata Tracking**: Document name, upload date, employee ID, file type
✅ **File Validation**: Type and size restrictions
✅ **Filter & Search**: By employee ID and document type

## Tech Stack

- **Backend**: Node.js + Express
- **Database**: MongoDB
- **File Upload**: Multer
- **Storage**: Local Storage / AWS S3
- **Frontend**: React

## Project Structure

```
backend/node-document-service/
├── controllers/
│   └── documentController.js    # Business logic
├── models/
│   └── Document.js              # MongoDB schema
├── routes/
│   └── documentRoutes.js        # API routes
├── middleware/
│   ├── upload.js                # Local storage (Multer)
│   └── s3Upload.js              # AWS S3 storage (optional)
├── uploads/                     # Local file storage
├── .env                         # Environment variables
├── server.js                    # Express server
└── package.json

frontend/src/components/DocumentManagement/
├── DocumentManagement.jsx       # Main container
├── DocumentUpload.jsx           # Upload component
├── DocumentList.jsx             # List & manage documents
└── DocumentManagement.css       # Styles
```

## Installation

### Backend Setup

1. Navigate to the service directory:
```bash
cd backend/node-document-service
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables in `.env`:
```env
MONGODB_URI=mongodb://localhost:27017/hr_management
DOC_SERVICE_PORT=5001
NODE_ENV=development

# Optional: AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

4. Start the server:
```bash
npm start
# or for development with auto-reload
npm run dev
```

### Frontend Setup

1. Install axios if not already installed:
```bash
cd frontend
npm install axios
```

2. Import the component in your React app:
```javascript
import DocumentManagement from './components/DocumentManagement/DocumentManagement';

function App() {
  return (
    <div>
      <DocumentManagement />
    </div>
  );
}
```

## API Endpoints

### Upload Document
```http
POST /api/documents/upload
Content-Type: multipart/form-data

Body:
- document: File
- employeeId: String
- documentType: String (resume|certificate|offer_letter|employee_report|other)
- uploadedBy: String
```

### Get All Documents
```http
GET /api/documents?employeeId=EMP001&documentType=resume
```

### Get Document by ID
```http
GET /api/documents/:id
```

### Download Document
```http
GET /api/documents/:id/download
```

### Delete Document
```http
DELETE /api/documents/:id
```

### Get Document Versions
```http
GET /api/documents/:id/versions
```

## MongoDB Schema

```javascript
{
  documentName: String,        // Stored filename
  originalName: String,        // Original filename
  employeeId: String,          // Employee identifier
  fileType: String,            // File extension
  documentType: String,        // Category (resume, certificate, etc.)
  fileSize: Number,            // Size in bytes
  filePath: String,            // Local path or S3 key
  s3Key: String,               // AWS S3 key (if using S3)
  uploadDate: Date,            // Upload timestamp
  version: Number,             // Current version
  previousVersions: [{         // Version history
    documentName: String,
    filePath: String,
    s3Key: String,
    version: Number,
    uploadDate: Date
  }],
  uploadedBy: String,          // User who uploaded
  metadata: Map,               // Additional metadata
  timestamps: true             // createdAt, updatedAt
}
```

## Version Control

The system automatically handles document versioning:

1. When uploading a document with the same name, employee ID, and type
2. Previous version is stored in `previousVersions` array
3. New version number is incremented
4. All versions are preserved until document is deleted

## Storage Options

### Local Storage (Default)
Files are stored in `backend/node-document-service/uploads/`

### AWS S3 Storage
To use AWS S3:

1. Install AWS SDK:
```bash
npm install aws-sdk multer-s3
```

2. Update `.env` with AWS credentials

3. Modify `server.js` to use S3 upload:
```javascript
const { uploadS3 } = require('./middleware/s3Upload');
// Replace upload.single() with uploadS3.single()
```

## File Validation

- **Allowed Types**: PDF, DOC, DOCX, JPG, JPEG, PNG, TXT, XLS, XLSX
- **Max Size**: 10MB
- **Validation**: Server-side and client-side

## Security Features

- File type validation
- File size limits
- Private S3 bucket access (if using S3)
- Secure file paths
- Input sanitization

## Usage Example

```javascript
// Upload a document
const formData = new FormData();
formData.append('document', file);
formData.append('employeeId', 'EMP001');
formData.append('documentType', 'resume');
formData.append('uploadedBy', 'HR Admin');

const response = await axios.post(
  'http://localhost:5001/api/documents/upload',
  formData
);

// Get documents for an employee
const docs = await axios.get(
  'http://localhost:5001/api/documents?employeeId=EMP001'
);

// Download a document
const blob = await axios.get(
  `http://localhost:5001/api/documents/${docId}/download`,
  { responseType: 'blob' }
);
```

## Testing

Test the API using curl:

```bash
# Upload document
curl -X POST http://localhost:5001/api/documents/upload \
  -F "document=@/path/to/file.pdf" \
  -F "employeeId=EMP001" \
  -F "documentType=resume" \
  -F "uploadedBy=HR Admin"

# Get all documents
curl http://localhost:5001/api/documents

# Download document
curl http://localhost:5001/api/documents/{id}/download -o downloaded.pdf
```

## Troubleshooting

**MongoDB Connection Error**
- Ensure MongoDB is running: `mongod`
- Check connection string in `.env`

**File Upload Fails**
- Check file size (max 10MB)
- Verify file type is allowed
- Ensure uploads directory exists and has write permissions

**CORS Issues**
- Backend CORS is enabled for all origins in development
- For production, configure specific origins in `server.js`

## Production Deployment

1. Set `NODE_ENV=production` in `.env`
2. Configure specific CORS origins
3. Use AWS S3 for scalable storage
4. Enable HTTPS
5. Add authentication middleware
6. Implement rate limiting
7. Set up monitoring and logging

## Future Enhancements

- [ ] Document preview functionality
- [ ] Bulk upload support
- [ ] Advanced search and filtering
- [ ] Document sharing with permissions
- [ ] Audit logs for document access
- [ ] OCR for document text extraction
- [ ] Document expiry notifications

## License

MIT License
