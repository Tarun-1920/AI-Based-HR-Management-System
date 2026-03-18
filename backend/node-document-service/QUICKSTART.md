# Quick Start Guide - Document Management Module

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd backend/node-document-service
npm install
```

### Step 2: Start MongoDB

Make sure MongoDB is running on your system:
```bash
mongod
```

### Step 3: Start the Document Service

```bash
npm start
```

You should see:
```
MongoDB connected
Document Management Service running on port 5001
```

### Step 4: Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:5001/health
```

### Step 5: Integrate with React Frontend

In your React app (frontend/src/App.js or any page):

```javascript
import DocumentManagement from './components/DocumentManagement/DocumentManagement';

function HRDashboard() {
  return (
    <div>
      <h1>HR Dashboard</h1>
      <DocumentManagement />
    </div>
  );
}
```

### Step 6: Start React App

```bash
cd frontend
npm start
```

Visit: http://localhost:3000

## 📝 Quick Test

### Upload a Document via API

```bash
curl -X POST http://localhost:5001/api/documents/upload \
  -F "document=@C:/path/to/resume.pdf" \
  -F "employeeId=EMP001" \
  -F "documentType=resume" \
  -F "uploadedBy=HR Admin"
```

### Get All Documents

```bash
curl http://localhost:5001/api/documents
```

### Filter by Employee

```bash
curl "http://localhost:5001/api/documents?employeeId=EMP001"
```

## 🎯 Key Features to Test

1. **Upload**: Select a file and upload
2. **View**: See all documents in the table
3. **Filter**: Filter by document type
4. **Download**: Click download button
5. **Delete**: Remove a document
6. **Version Control**: Upload same file again to see versioning

## 🔧 Configuration

Edit `backend/node-document-service/.env`:

```env
MONGODB_URI=mongodb://localhost:27017/hr_management
DOC_SERVICE_PORT=5001
```

## 📦 Supported File Types

- PDF (.pdf)
- Word (.doc, .docx)
- Images (.jpg, .jpeg, .png)
- Text (.txt)
- Excel (.xls, .xlsx)

Max file size: 10MB

## 🐛 Common Issues

**Port 5001 already in use?**
```bash
# Change port in .env
DOC_SERVICE_PORT=5002
```

**MongoDB not connecting?**
```bash
# Check if MongoDB is running
mongod --version
```

**CORS error in React?**
- Backend already has CORS enabled
- Make sure backend is running on port 5001

## ✅ Success Checklist

- [ ] MongoDB running
- [ ] Backend service running on port 5001
- [ ] React app running on port 3000
- [ ] Can upload a document
- [ ] Can view documents
- [ ] Can download documents
- [ ] Can delete documents

## 🎉 You're Ready!

The Document Management Module is now fully functional!
