# Document Management UI Guide

## Component Overview

### Main Container: DocumentManagement
The primary component that orchestrates the entire document management interface.

```
┌─────────────────────────────────────────────────────────────┐
│                  Document Management System                  │
├─────────────────────────────────────────────────────────────┤
│  Filter by Employee ID: [_______________]                    │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                   │
│   Upload Document        │      Documents                    │
│   ┌──────────────────┐   │   ┌──────────────────────────┐  │
│   │ Document Type:   │   │   │ Filter: [All Types ▼]    │  │
│   │ [Resume      ▼]  │   │   └──────────────────────────┘  │
│   │                  │   │                                   │
│   │ Select File:     │   │   ┌──────────────────────────┐  │
│   │ [Choose File]    │   │   │ Name  Type  EmpID  Date  │  │
│   │ resume.pdf       │   │   ├──────────────────────────┤  │
│   │                  │   │   │ doc1  Resume EMP001 ...  │  │
│   │ [Upload Document]│   │   │ [Download] [Delete]      │  │
│   │                  │   │   ├──────────────────────────┤  │
│   │ ✓ Upload success!│   │   │ doc2  Cert  EMP001 ...   │  │
│   └──────────────────┘   │   │ [Download] [Delete]      │  │
│                          │   └──────────────────────────┘  │
└──────────────────────────┴──────────────────────────────────┘
```

## Component Breakdown

### 1. DocumentUpload Component

**Purpose**: Handle file selection and upload

**Features**:
- Document type dropdown (Resume, Certificate, Offer Letter, etc.)
- File input with validation
- Upload button with loading state
- Success/error message display

**User Flow**:
```
1. Select document type from dropdown
2. Click "Choose File" button
3. Select file from computer
4. File name appears below input
5. Click "Upload Document"
6. Button shows "Uploading..." during upload
7. Success message appears
8. Form resets for next upload
```

**Visual States**:
```
Initial State:
┌──────────────────┐
│ Document Type:   │
│ [Resume      ▼]  │
│                  │
│ Select File:     │
│ [Choose File]    │
│                  │
│ [Upload Document]│ ← Disabled
└──────────────────┘

File Selected:
┌──────────────────┐
│ Document Type:   │
│ [Resume      ▼]  │
│                  │
│ Select File:     │
│ [Choose File]    │
│ 📄 resume.pdf    │ ← File name shown
│                  │
│ [Upload Document]│ ← Enabled
└──────────────────┘

Uploading:
┌──────────────────┐
│ Document Type:   │
│ [Resume      ▼]  │
│                  │
│ Select File:     │
│ [Choose File]    │
│ 📄 resume.pdf    │
│                  │
│ [Uploading...]   │ ← Disabled
└──────────────────┘

Success:
┌──────────────────┐
│ Document Type:   │
│ [Resume      ▼]  │
│                  │
│ Select File:     │
│ [Choose File]    │
│                  │
│ [Upload Document]│
│                  │
│ ✓ Upload success!│ ← Green message
└──────────────────┘
```

### 2. DocumentList Component

**Purpose**: Display, filter, and manage documents

**Features**:
- Document type filter
- Sortable table
- Download functionality
- Delete with confirmation
- Version display
- Empty state

**Table Columns**:
```
┌──────────────┬──────────┬──────────┬────────────┬────────┬─────────┬──────────────┐
│ Document Name│   Type   │ Emp ID   │ Upload Date│  Size  │ Version │   Actions    │
├──────────────┼──────────┼──────────┼────────────┼────────┼─────────┼──────────────┤
│ resume.pdf   │ Resume   │ EMP001   │ 01/15/2024 │ 240 KB │   v2    │ [↓] [🗑]     │
│ cert.jpg     │ Cert     │ EMP001   │ 01/14/2024 │ 156 KB │   v1    │ [↓] [🗑]     │
│ offer.pdf    │ Offer    │ EMP002   │ 01/13/2024 │ 89 KB  │   v1    │ [↓] [🗑]     │
└──────────────┴──────────┴──────────┴────────────┴────────┴─────────┴──────────────┘
```

**Filter Options**:
```
┌──────────────────┐
│ All Types    ▼   │
├──────────────────┤
│ All Types        │
│ Resume           │
│ Certificate      │
│ Offer Letter     │
│ Employee Report  │
│ Other            │
└──────────────────┘
```

**Empty State**:
```
┌─────────────────────────────┐
│                             │
│    📄 No documents found    │
│                             │
└─────────────────────────────┘
```

**Loading State**:
```
┌─────────────────────────────┐
│                             │
│    ⏳ Loading documents...  │
│                             │
└─────────────────────────────┘
```

## Color Scheme

### Document Type Badges
```
Resume:          [Resume]         Blue (#e3f2fd / #1976d2)
Certificate:     [Certificate]    Green (#e8f5e9 / #388e3c)
Offer Letter:    [Offer Letter]   Purple (#f3e5f5 / #7b1fa2)
Employee Report: [Report]         Orange (#fff3e0 / #f57c00)
Other:           [Other]          Gray (#f5f5f5 / #616161)
```

### Buttons
```
Upload:   Blue (#3498db)    Hover: (#2980b9)
Download: Green (#27ae60)   Hover: (#229954)
Delete:   Red (#e74c3c)     Hover: (#c0392b)
```

### Messages
```
Success: Green background (#d4edda) with dark green text (#155724)
Error:   Red background (#f8d7da) with dark red text (#721c24)
```

## Responsive Behavior

### Desktop (> 1024px)
```
┌─────────────────────────────────────────────────┐
│  [Upload Panel]  │  [Document List Panel]       │
│  (1/3 width)     │  (2/3 width)                 │
└─────────────────────────────────────────────────┘
```

### Tablet/Mobile (< 1024px)
```
┌─────────────────────────────────────────────────┐
│  [Upload Panel]                                 │
│  (Full width)                                   │
├─────────────────────────────────────────────────┤
│  [Document List Panel]                          │
│  (Full width, stacked below)                    │
└─────────────────────────────────────────────────┘
```

## User Interactions

### Upload Document
```
1. User Action: Select document type
   → Dropdown opens with options

2. User Action: Click "Choose File"
   → File browser opens

3. User Action: Select file
   → File name appears
   → Upload button enables

4. User Action: Click "Upload Document"
   → Button shows "Uploading..."
   → Button disables
   → Progress indication

5. System Response: Upload complete
   → Success message appears
   → Form resets
   → Document list refreshes
```

### Download Document
```
1. User Action: Click download button
   → Button shows loading state

2. System Response: File streams
   → Browser download dialog appears

3. User Action: Choose save location
   → File downloads to computer
```

### Delete Document
```
1. User Action: Click delete button
   → Confirmation dialog appears
   → "Are you sure you want to delete this document?"

2. User Action: Click "OK"
   → Delete request sent
   → Row fades out
   → Document list refreshes

   OR

   User Action: Click "Cancel"
   → Dialog closes
   → No action taken
```

### Filter Documents
```
1. User Action: Enter Employee ID
   → List filters in real-time
   → Shows only matching documents

2. User Action: Select document type
   → List filters immediately
   → Shows only selected type

3. User Action: Clear filters
   → All documents shown again
```

## Accessibility Features

- **Keyboard Navigation**: All buttons and inputs accessible via Tab
- **Screen Reader Support**: Proper labels and ARIA attributes
- **Focus Indicators**: Clear focus states on all interactive elements
- **Color Contrast**: WCAG AA compliant color combinations
- **Error Messages**: Clear, descriptive error messages

## Integration Example

### Basic Integration
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

### With Custom Employee ID
```javascript
import { DocumentUpload, DocumentList } from './components/DocumentManagement';

function EmployeeProfile({ employeeId }) {
  return (
    <div>
      <h2>Employee Documents</h2>
      <DocumentUpload employeeId={employeeId} />
      <DocumentList employeeId={employeeId} />
    </div>
  );
}
```

### With Custom Styling
```javascript
import DocumentManagement from './components/DocumentManagement/DocumentManagement';
import './custom-document-styles.css';

function CustomDocuments() {
  return (
    <div className="custom-wrapper">
      <DocumentManagement />
    </div>
  );
}
```

## Tips for Customization

### Change Colors
Edit `DocumentManagement.css`:
```css
/* Primary button color */
.document-upload button {
  background: #your-color;
}

/* Document type badge */
.doc-type {
  background: #your-bg-color;
  color: #your-text-color;
}
```

### Add New Document Types
Edit `documentController.js` and `Document.js`:
```javascript
// In Document.js schema
documentType: { 
  type: String, 
  enum: ['resume', 'certificate', 'offer_letter', 'employee_report', 'your_new_type'],
  required: true 
}
```

Then update the dropdown in `DocumentUpload.jsx`:
```javascript
<option value="your_new_type">Your New Type</option>
```

### Modify File Size Limit
Edit `upload.js`:
```javascript
limits: { fileSize: 20 * 1024 * 1024 }, // 20MB
```

### Add More File Types
Edit `upload.js`:
```javascript
const allowedTypes = /pdf|doc|docx|jpg|jpeg|png|txt|xlsx|xls|your_new_type/;
```

---

**UI Version**: 1.0
**Last Updated**: 2024
