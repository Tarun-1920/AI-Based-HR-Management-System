# AI-Based HR Management System - Frontend

A modern, responsive React frontend for an AI-powered HR management system focused on recruitment and candidate screening.

## 🚀 Features

- **Modern UI Design**: Clean, professional interface with gradient themes
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Role-Based Access**: Different interfaces for HR managers and candidates
- **AI-Powered Matching**: Visual representation of AI candidate matching scores
- **Real-time Updates**: Dynamic status updates and notifications
- **File Upload**: Drag-and-drop resume upload with progress indicators

## 📁 Project Structure

```
src/
├── components/
│   └── Sidebar.js          # Navigation sidebar component
├── pages/
│   ├── Login.js            # Authentication page
│   ├── Dashboard.js        # Main dashboard (HR & Candidate views)
│   ├── PostJob.js          # Job posting form
│   ├── UploadResume.js     # Resume upload page
│   └── Candidates.js       # Candidate management & ranking
├── styles/
│   ├── App.css             # Global styles and common components
│   ├── Sidebar.css         # Sidebar navigation styles
│   ├── Login.css           # Login page styles
│   ├── Dashboard.css       # Dashboard styles
│   ├── PostJob.css         # Job posting form styles
│   ├── UploadResume.css    # Resume upload styles
│   └── Candidates.css      # Candidate management styles
├── utils/
│   └── api.js              # API utility functions
├── App.js                  # Main app component with routing
└── index.js                # React entry point
```

## 🛠️ Technologies Used

- **React 18** - Modern React with functional components and hooks
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with flexbox, grid, and animations
- **Font Awesome** - Icons and visual elements

## 🎨 Design Features

- **Gradient Themes**: Beautiful purple-blue gradients throughout
- **Card-Based Layout**: Clean card designs for better content organization
- **Smooth Animations**: Hover effects, transitions, and loading states
- **Professional Typography**: Clean, readable fonts with proper hierarchy
- **Color-Coded Status**: Visual indicators for different states and scores
- **Interactive Elements**: Hover effects and smooth transitions

## 📱 Pages Overview

### 1. Login Page
- Role-based authentication (HR Manager / Candidate)
- Modern card design with gradient background
- Demo credentials provided for testing

### 2. Dashboard
- **HR Dashboard**: Stats cards, recent activities, top candidates
- **Candidate Dashboard**: Welcome section, application status
- Real-time data visualization

### 3. Job Posting (HR Only)
- Comprehensive job posting form
- Required skills input for AI matching
- Form validation and success feedback

### 4. Resume Upload (Candidates Only)
- Drag-and-drop file upload
- Personal information form
- AI processing simulation with status updates
- Supported formats: PDF, DOCX

### 5. Candidate Management (HR Only)
- AI-powered candidate ranking
- Advanced filtering and search
- Match score visualization
- Status management (New, Reviewed, Shortlisted, etc.)
- Bulk actions and candidate details

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Demo Credentials

**HR Manager:**
- Email: hr@company.com
- Password: password123

**Candidate:**
- Email: candidate@email.com
- Password: password123

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

### API Integration
The frontend is designed to work with a Flask backend. API endpoints are configured in `src/utils/api.js`.

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: 767px and below

## 🎯 Key Components

### Sidebar Navigation
- Role-based menu items
- Active state indicators
- User information display
- Logout functionality

### File Upload Component
- Drag-and-drop interface
- File type validation
- Upload progress indication
- Error handling

### Candidate Cards
- Match score visualization
- Skills display with tags
- Status badges with colors
- Action buttons for HR

## 🔮 Future Enhancements

- Dark mode toggle
- Advanced filtering options
- Real-time notifications
- Chat functionality
- Video interview integration
- Advanced analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of an AI-Based HR Management System MVP.

---

**Note**: This is the frontend component of the MVP. It requires a backend API to be fully functional. The UI includes mock data for demonstration purposes.