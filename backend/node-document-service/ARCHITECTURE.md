# Document Management Module - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 3000)               │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ DocumentUpload   │  │  DocumentList    │                │
│  │  - File select   │  │  - View docs     │                │
│  │  - Type select   │  │  - Download      │                │
│  │  - Upload button │  │  - Delete        │                │
│  └────────┬─────────┘  └────────┬─────────┘                │
│           │                     │                           │
│           └──────────┬──────────┘                           │
│                      │                                      │
│           ┌──────────▼──────────┐                          │
│           │ DocumentManagement  │                          │
│           │   (Main Container)  │                          │
│           └──────────┬──────────┘                          │
└──────────────────────┼──────────────────────────────────────┘
                       │ HTTP/Axios
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Node.js Express Server (Port 5001)             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Routes (documentRoutes.js)          │  │
│  │  POST   /api/documents/upload                        │  │
│  │  GET    /api/documents                               │  │
│  │  GET    /api/documents/:id                           │  │
│  │  GET    /api/documents/:id/download                  │  │
│  │  DELETE /api/documents/:id                           │  │
│  │  GET    /api/documents/:id/versions                  │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         Multer Middleware (upload.js)                │  │
│  │  - File validation                                   │  │
│  │  - Size check (10MB)                                 │  │
│  │  - Type check (pdf, doc, jpg, etc.)                  │  │
│  │  - Storage handling                                  │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │      Document Controller (documentController.js)     │  │
│  │  - uploadDocument()                                  │  │
│  │  - getDocuments()                                    │  │
│  │  - getDocumentById()                                 │  │
│  │  - downloadDocument()                                │  │
│  │  - deleteDocument()                                  │  │
│  │  - getDocumentVersions()                             │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         Mongoose Model (Document.js)                 │  │
│  │  - Schema definition                                 │  │
│  │  - Validation rules                                  │  │
│  │  - Indexes                                           │  │
│  └────────────────────┬─────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                    MongoDB Database                          │
├─────────────────────────────────────────────────────────────┤
│  Collection: documents                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ {                                                    │   │
│  │   _id: ObjectId,                                     │   │
│  │   documentName: "1234567890-resume.pdf",            │   │
│  │   originalName: "resume.pdf",                        │   │
│  │   employeeId: "EMP001",                              │   │
│  │   fileType: "pdf",                                   │   │
│  │   documentType: "resume",                            │   │
│  │   fileSize: 245678,                                  │   │
│  │   filePath: "/uploads/1234567890-resume.pdf",       │   │
│  │   uploadDate: ISODate("2024-01-15"),                │   │
│  │   version: 2,                                        │   │
│  │   previousVersions: [                                │   │
│  │     { version: 1, filePath: "...", uploadDate: ... }│   │
│  │   ],                                                 │   │
│  │   uploadedBy: "HR Admin"                             │   │
│  │ }                                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                  File Storage                                │
├─────────────────────────────────────────────────────────────┤
│  Option 1: Local Storage                                    │
│  └─ /backend/node-document-service/uploads/                 │
│                                                              │
│  Option 2: AWS S3 (Optional)                                │
│  └─ s3://your-bucket/documents/                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Upload Flow
```
1. User selects file in React UI
   ↓
2. FormData created with file + metadata
   ↓
3. POST request to /api/documents/upload
   ↓
4. Multer middleware processes file
   ↓
5. File saved to storage (local/S3)
   ↓
6. Controller checks for existing document
   ↓
7. Version number calculated
   ↓
8. Document metadata saved to MongoDB
   ↓
9. Success response sent to frontend
   ↓
10. UI updates with new document
```

### Download Flow
```
1. User clicks download button
   ↓
2. GET request to /api/documents/:id/download
   ↓
3. Controller retrieves document from MongoDB
   ↓
4. File streamed from storage
   ↓
5. Browser receives file as blob
   ↓
6. File downloaded to user's computer
```

### Version Control Flow
```
1. User uploads document with same name
   ↓
2. System searches for existing document
   ↓
3. If found:
   - Current version moved to previousVersions[]
   - Version number incremented
   - New document saved with new version
   ↓
4. If not found:
   - New document created with version 1
```

## Component Hierarchy

```
DocumentManagement (Container)
├── Employee Filter Input
├── DocumentUpload
│   ├── Document Type Selector
│   ├── File Input
│   ├── Upload Button
│   └── Status Message
└── DocumentList
    ├── Type Filter Dropdown
    ├── Document Table
    │   ├── Document Name
    │   ├── Type Badge
    │   ├── Employee ID
    │   ├── Upload Date
    │   ├── File Size
    │   ├── Version Number
    │   └── Action Buttons
    │       ├── Download Button
    │       └── Delete Button
    └── Empty State
```

## API Request/Response Examples

### Upload Document
```javascript
// Request
POST /api/documents/upload
Content-Type: multipart/form-data

FormData:
- document: [File]
- employeeId: "EMP001"
- documentType: "resume"
- uploadedBy: "HR Admin"

// Response
{
  "message": "Document uploaded successfully",
  "document": {
    "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "documentName": "1705334567890-resume.pdf",
    "originalName": "resume.pdf",
    "employeeId": "EMP001",
    "fileType": "pdf",
    "documentType": "resume",
    "fileSize": 245678,
    "version": 1,
    "uploadDate": "2024-01-15T10:30:00.000Z"
  }
}
```

### Get Documents
```javascript
// Request
GET /api/documents?employeeId=EMP001&documentType=resume

// Response
{
  "documents": [
    {
      "_id": "65a1b2c3d4e5f6g7h8i9j0k1",
      "documentName": "1705334567890-resume.pdf",
      "originalName": "resume.pdf",
      "employeeId": "EMP001",
      "documentType": "resume",
      "version": 2,
      "uploadDate": "2024-01-15T10:30:00.000Z"
    }
  ]
}
```

## Security Layers

```
┌─────────────────────────────────────┐
│  1. Client-Side Validation          │
│     - File type check               │
│     - File size check               │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Multer Middleware               │
│     - File type validation          │
│     - Size limit enforcement        │
│     - Filename sanitization         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Controller Validation           │
│     - Required fields check         │
│     - Input sanitization            │
│     - Business logic validation     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. MongoDB Schema Validation       │
│     - Data type validation          │
│     - Required fields               │
│     - Enum constraints              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  5. Storage Security                │
│     - Private file paths            │
│     - S3 private buckets (optional) │
│     - Access control                │
└─────────────────────────────────────┘
```

## Database Indexes

```javascript
// Compound index for efficient queries
{ employeeId: 1, documentType: 1 }

// Single field index
{ employeeId: 1 }

// Use cases:
// - Find all documents for an employee
// - Find specific document type for an employee
// - Fast filtering and sorting
```

## File Storage Structure

### Local Storage
```
backend/node-document-service/uploads/
├── 1705334567890-123456789-resume.pdf
├── 1705334568901-234567890-certificate.pdf
├── 1705334569012-345678901-offer_letter.pdf
└── ...
```

### AWS S3 Storage
```
s3://your-bucket/
└── documents/
    ├── EMP001/
    │   ├── 1705334567890-resume.pdf
    │   └── 1705334568901-certificate.pdf
    ├── EMP002/
    │   └── 1705334569012-resume.pdf
    └── ...
```

## Performance Considerations

1. **Indexing**: MongoDB indexes on employeeId and documentType
2. **Pagination**: Can be added for large document lists
3. **Caching**: Consider Redis for frequently accessed metadata
4. **CDN**: Use CloudFront with S3 for faster downloads
5. **Compression**: Compress large files before storage
6. **Lazy Loading**: Load documents on-demand in UI

## Scalability

- **Horizontal Scaling**: Multiple Node.js instances behind load balancer
- **Database Sharding**: Shard MongoDB by employeeId
- **Storage**: S3 provides unlimited scalability
- **Microservice**: Isolated service can scale independently

## Monitoring Points

- Upload success/failure rate
- Average upload time
- Storage usage
- API response times
- Error rates
- Document access patterns

---

**Architecture Version**: 1.0
**Last Updated**: 2024
