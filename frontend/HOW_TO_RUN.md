# How to Run the Frontend - Step by Step Guide

## Prerequisites

Before running the frontend, make sure you have the following installed:

### Required Software
1. **Node.js** (v14 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **npm** (comes with Node.js)
   - Verify installation: `npm --version`

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/

---

## Quick Start (5 minutes)

### Step 1: Navigate to Frontend Directory
```bash
cd "c:\Users\tharu\OneDrive\Desktop\AI-Baesd HR_Management_System\frontend"
```

### Step 2: Install Dependencies
```bash
npm install
```
This will install all required packages from `package.json`

### Step 3: Start Development Server
```bash
npm start
```

### Step 4: Open in Browser
- Automatically opens: http://localhost:3000
- If not, manually open: http://localhost:3000

### Step 5: Login
Use demo credentials:
- **Email**: demo@example.com
- **Password**: demo123
- **Role**: HR Manager or Candidate

---

## Detailed Setup Instructions

### 1. Install Node.js

**Windows**:
1. Download from https://nodejs.org/
2. Run the installer
3. Follow installation wizard
4. Restart your computer

**Verify Installation**:
```bash
node --version
npm --version
```

### 2. Navigate to Project

**Using Command Prompt**:
```bash
cd "c:\Users\tharu\OneDrive\Desktop\AI-Baesd HR_Management_System\frontend"
```

**Or using PowerShell**:
```powershell
cd "c:\Users\tharu\OneDrive\Desktop\AI-Baesd HR_Management_System\frontend"
```

### 3. Install Dependencies

```bash
npm install
```

**What this does**:
- Reads `package.json`
- Downloads all required packages
- Creates `node_modules` folder
- Generates `package-lock.json`

**Expected output**:
```
added 1234 packages in 2m
```

### 4. Create Environment File

Create `.env` file in the frontend root directory:

```bash
# Windows Command Prompt
echo REACT_APP_API_URL=http://localhost:5000/api > .env

# Or create manually
# File: frontend/.env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### 5. Start Development Server

```bash
npm start
```

**Expected output**:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### 6. Access the Application

Open your browser and go to:
```
http://localhost:3000
```

---

## Available Scripts

### Development
```bash
npm start
```
- Runs the app in development mode
- Opens http://localhost:3000
- Hot reloads on file changes
- Shows errors in console

### Build for Production
```bash
npm run build
```
- Creates optimized production build
- Output in `build/` folder
- Ready for deployment

### Run Tests
```bash
npm test
```
- Runs test suite
- Watches for changes
- Press `q` to quit

### Eject Configuration
```bash
npm run eject
```
⚠️ **Warning**: This is irreversible!
- Exposes all configuration
- Only use if you need custom setup

---

## Troubleshooting

### Issue 1: "npm: command not found"

**Solution**:
1. Node.js not installed
2. Install from https://nodejs.org/
3. Restart terminal/computer
4. Verify: `npm --version`

### Issue 2: "Port 3000 already in use"

**Solution A**: Kill the process using port 3000
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm start
```

**Solution B**: Use different port
```bash
set PORT=3001 && npm start
```

### Issue 3: "Module not found" error

**Solution**:
```bash
# Clear node_modules
rmdir /s /q node_modules
del package-lock.json

# Reinstall
npm install

# Start again
npm start
```

### Issue 4: "Cannot find module 'react'"

**Solution**:
```bash
# Make sure you're in frontend directory
cd frontend

# Reinstall dependencies
npm install

# Start
npm start
```

### Issue 5: Blank page or errors

**Solution**:
1. Open DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for API calls
4. Clear browser cache (Ctrl+Shift+Delete)
5. Hard refresh (Ctrl+Shift+R)

### Issue 6: "EACCES: permission denied"

**Solution** (Mac/Linux):
```bash
sudo npm install
sudo npm start
```

---

## Project Structure

```
frontend/
├── public/
│   └── index.html              # Main HTML file
├── src/
│   ├── components/             # Reusable components
│   ├── pages/                  # Page components
│   ├── styles/                 # CSS files
│   ├── utils/                  # Utility functions
│   ├── App.js                  # Main app component
│   └── index.js                # React entry point
├── package.json                # Dependencies
├── .env                        # Environment variables
└── README.md                   # Documentation
```

---

## Testing the Application

### 1. Login Page
- URL: http://localhost:3000/login
- Use demo credentials
- Test form validation
- Test error messages

### 2. Dashboard
- View statistics
- Check recent activities
- See top candidates
- Test role-specific views

### 3. Post Job
- Fill job form
- Test validation
- Submit job
- Check success message

### 4. Upload Resume
- Drag and drop file
- Test file validation
- Upload resume
- Check progress bar

### 5. Candidate Ranking
- View candidates table
- Test search functionality
- Test filtering
- Test sorting

---

## Development Tips

### Hot Reload
- Changes to files automatically reload
- No need to restart server
- Check browser console for errors

### Browser DevTools
- Press F12 to open
- Console tab: See errors and logs
- Network tab: See API calls
- Elements tab: Inspect HTML/CSS

### Debugging
```javascript
// Add console logs
console.log('Variable:', variable);

// Use debugger
debugger;

// Check localStorage
localStorage.getItem('authToken');
```

### Testing Without Backend
- App has mock data fallback
- Dashboard shows mock statistics
- Job posting has mock jobs
- Candidate ranking shows mock candidates

---

## Environment Variables

### Development (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### Production (.env.production)
```
REACT_APP_API_URL=https://api.yourdomain.com/api
REACT_APP_ENV=production
```

### Using Environment Variables
```javascript
// In code
const apiUrl = process.env.REACT_APP_API_URL;
const env = process.env.REACT_APP_ENV;
```

---

## Performance Tips

### 1. Clear Cache
```bash
npm cache clean --force
```

### 2. Update npm
```bash
npm install -g npm@latest
```

### 3. Check for Vulnerabilities
```bash
npm audit
npm audit fix
```

### 4. Update Dependencies
```bash
npm outdated
npm update
```

---

## Building for Production

### Step 1: Create Production Build
```bash
npm run build
```

### Step 2: Test Production Build Locally
```bash
npm install -g serve
serve -s build
```

### Step 3: Deploy
- Upload `build/` folder to hosting
- Set environment variables
- Configure backend API URL

---

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies |
| `npm start` | Start development server |
| `npm run build` | Create production build |
| `npm test` | Run tests |
| `npm run eject` | Eject configuration |
| `npm cache clean --force` | Clear npm cache |
| `npm outdated` | Check for updates |
| `npm update` | Update dependencies |
| `npm audit` | Check vulnerabilities |
| `npm audit fix` | Fix vulnerabilities |

---

## File Locations

### Important Files
- **Main App**: `src/App.js`
- **Entry Point**: `src/index.js`
- **API Service**: `src/utils/api.js`
- **Styles**: `src/styles/`
- **Components**: `src/components/`
- **Pages**: `src/pages/`
- **Environment**: `.env`
- **Dependencies**: `package.json`

---

## Accessing Different Pages

### Login Page
```
http://localhost:3000/login
```

### Dashboard
```
http://localhost:3000/dashboard
```

### Post Job
```
http://localhost:3000/post-job
```

### Upload Resume
```
http://localhost:3000/upload-resume
```

### Candidate Ranking
```
http://localhost:3000/candidates
```

---

## Demo Credentials

### HR Manager
- **Email**: demo@example.com
- **Password**: demo123
- **Role**: HR Manager

### Candidate
- **Email**: candidate@example.com
- **Password**: demo123
- **Role**: Candidate

---

## Stopping the Server

### Method 1: Keyboard Shortcut
```
Press Ctrl + C
```

### Method 2: Close Terminal
- Close the terminal window

### Method 3: Kill Process
```bash
# Windows
taskkill /F /IM node.exe

# Mac/Linux
killall node
```

---

## Next Steps

### After Running Frontend
1. ✅ Explore the UI
2. ✅ Test all pages
3. ✅ Check responsive design (F12 → Toggle device toolbar)
4. ✅ Review component code
5. ⏳ Wait for backend to be implemented

### To Connect Backend
1. Implement backend API (see `BACKEND_INTEGRATION_GUIDE.md`)
2. Update `REACT_APP_API_URL` in `.env`
3. Restart frontend
4. Test API integration

### To Deploy
1. Build: `npm run build`
2. Deploy `build/` folder
3. Set environment variables
4. Configure backend URL

---

## Getting Help

### Documentation
- `README.md` - Project overview
- `SETUP.md` - Setup instructions
- `QUICKSTART.md` - Quick start guide
- `PRODUCTION_GUIDE.md` - Production guide
- `BACKEND_INTEGRATION_GUIDE.md` - Backend setup

### Code Examples
- Check component files in `src/components/`
- Review page files in `src/pages/`
- See API usage in `src/utils/api.js`

### External Resources
- [React Documentation](https://react.dev/)
- [Node.js Documentation](https://nodejs.org/docs/)
- [npm Documentation](https://docs.npmjs.com/)

---

## Summary

### Quick Start
```bash
cd frontend
npm install
npm start
```

### Access Application
```
http://localhost:3000
```

### Demo Login
```
Email: demo@example.com
Password: demo123
```

### Stop Server
```
Ctrl + C
```

---

## Checklist

- [ ] Node.js installed
- [ ] npm installed
- [ ] Navigated to frontend directory
- [ ] Ran `npm install`
- [ ] Created `.env` file
- [ ] Ran `npm start`
- [ ] Opened http://localhost:3000
- [ ] Logged in with demo credentials
- [ ] Explored all pages
- [ ] Tested responsive design

---

**You're all set! The frontend is now running.** 🎉

For backend integration, see `BACKEND_INTEGRATION_GUIDE.md`
