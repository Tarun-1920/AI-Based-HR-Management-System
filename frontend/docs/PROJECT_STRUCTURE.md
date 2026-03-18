# Project Structure & File Organization Guide

## Directory Tree

```
frontend/
│
├── public/
│   └── index.html                          # Main HTML entry point
│
├── src/
│   │
│   ├── components/                         # Reusable UI Components
│   │   ├── Badge.js                       # Status/tag badge component
│   │   ├── Button.js                      # Reusable button with variants
│   │   ├── Card.js                        # Card layout component
│   │   ├── FormInput.js                   # Form input with validation
│   │   ├── LoadingSpinner.js              # Loading indicator component
│   │   ├── Modal.js                       # Modal/dialog component
│   │   ├── Sidebar.js                     # Navigation sidebar
│   │   ├── StatCard.js                    # Statistics display card
│   │   └── Toast.js                       # Toast notification component
│   │
│   ├── hooks/                              # Custom React Hooks
│   │   └── useToast.js                    # Toast notification management
│   │
│   ├── pages/                              # Page Components
│   │   ├── CandidateRanking.js            # Candidate ranking & management
│   │   ├── Dashboard.js                   # Main dashboard page
│   │   ├── Login.js                       # Authentication page
│   │   ├── PostJob.js                     # Job posting form page
│   │   └── UploadResume.js                # Resume upload page
│   │
│   ├── styles/                             # CSS Stylesheets
│   │   │
│   │   ├── components/                    # Component-Specific Styles
│   │   │   ├── Badge.css                 # Badge component styles
│   │   │   ├── Button.css                # Button component styles
│   │   │   ├── Card.css                  # Card component styles
│   │   │   ├── Components.css            # Shared component variables
│   │   │   ├── FormInput.css             # Form input styles
│   │   │   ├── Modal.css                 # Modal component styles
│   │   │   └── StatCard.css              # Stat card styles
│   │   │
│   │   ├── Animations.css                 # Animation library & effects
│   │   ├── App.css                        # Global application styles
│   │   ├── CandidateRanking.css           # Candidate ranking page styles
│   │   ├── Dashboard.css                  # Dashboard page styles
│   │   ├── Login.css                      # Login page styles
│   │   ├── PostJob.css                    # Job posting page styles
│   │   ├── ResponsiveMobile.css           # Mobile responsive styles
│   │   ├── Sidebar.css                    # Sidebar component styles
│   │   └── UploadResume.css               # Resume upload page styles
│   │
│   ├── utils/                              # Utility Functions & Services
│   │   └── api.js                         # API service layer & endpoints
│   │
│   ├── App.js                              # Main application component
│   └── index.js                            # React entry point
│
├── package.json                            # Project dependencies
├── README.md                               # Main project documentation
├── SETUP.md                                # Setup & installation guide
├── QUICKSTART.md                           # Quick start for developers
├── PRODUCTION_GUIDE.md                     # Production deployment guide
├── CLEANUP_SUMMARY.md                      # Cleanup & optimization summary
├── UI_IMPROVEMENTS.md                      # UI features documentation
└── UI_INTEGRATION_GUIDE.md                 # Component integration guide
```

## File Organization Principles

### 1. Components Directory (`src/components/`)
**Purpose**: Reusable UI components used across multiple pages

**Guidelines**:
- One component per file
- Component name matches filename (PascalCase)
- Include JSDoc comments
- Export default component
- Keep components focused and single-responsibility

**Example Structure**:
```javascript
/**
 * Button Component
 * Reusable button with multiple variants and sizes
 */
import React from 'react';
import '../styles/components/Button.css';

const Button = ({ variant, size, ...props }) => {
  // Component logic
};

export default Button;
```

### 2. Pages Directory (`src/pages/`)
**Purpose**: Full page components that represent routes

**Guidelines**:
- One page per file
- Page name matches filename (PascalCase)
- Import reusable components
- Handle page-level state
- Include page-specific logic

**Example Structure**:
```javascript
/**
 * Dashboard Page
 * Main dashboard with statistics and activities
 */
import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import StatCard from '../components/StatCard';
import '../styles/Dashboard.css';

const Dashboard = () => {
  // Page logic
};

export default Dashboard;
```

### 3. Styles Directory (`src/styles/`)
**Purpose**: All CSS files organized by scope

**Structure**:
- `components/` - Component-specific styles
- `*.css` - Page-specific styles
- `Animations.css` - Global animations
- `App.css` - Global styles
- `ResponsiveMobile.css` - Mobile responsive styles

**Guidelines**:
- Use CSS variables for consistency
- Organize by component/page
- Include responsive breakpoints
- Use meaningful class names
- Follow BEM naming convention

### 4. Utils Directory (`src/utils/`)
**Purpose**: Utility functions and services

**Current Files**:
- `api.js` - API service layer with all endpoints

**Guidelines**:
- One utility per file
- Export functions/classes
- Include error handling
- Add JSDoc comments
- Keep functions pure and reusable

### 5. Hooks Directory (`src/hooks/`)
**Purpose**: Custom React hooks

**Current Files**:
- `useToast.js` - Toast notification management

**Guidelines**:
- Hook name starts with `use`
- One hook per file
- Include JSDoc comments
- Return object with methods
- Handle cleanup in useEffect

## Naming Conventions

### Files
- **Components**: PascalCase (e.g., `Button.js`, `FormInput.js`)
- **Pages**: PascalCase (e.g., `Dashboard.js`, `Login.js`)
- **Hooks**: camelCase with `use` prefix (e.g., `useToast.js`)
- **Utils**: camelCase (e.g., `api.js`)
- **CSS**: kebab-case matching component (e.g., `form-input.css`)

### CSS Classes
- **Components**: `.component-name` (e.g., `.button`, `.form-input`)
- **Variants**: `.component-name-variant` (e.g., `.button-primary`)
- **States**: `.component-name.state` (e.g., `.button.disabled`)
- **Modifiers**: `.component-name--modifier` (e.g., `.button--large`)

### JavaScript Variables
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- **Functions**: camelCase (e.g., `handleClick`, `fetchData`)
- **Variables**: camelCase (e.g., `userData`, `isLoading`)
- **Classes**: PascalCase (e.g., `UserService`)

## Import/Export Patterns

### Component Imports
```javascript
// ✅ Good
import Button from '../components/Button';
import { useToast } from '../hooks/useToast';
import '../styles/Dashboard.css';

// ❌ Avoid
import * as components from '../components';
import Button from '../components/Button.js';
```

### API Imports
```javascript
// ✅ Good
import { authAPI, jobsAPI, candidatesAPI } from '../utils/api';

// ❌ Avoid
import api from '../utils/api';
const { authAPI } = api;
```

## CSS Organization

### Global Styles (`App.css`)
```css
/* Reset and base styles */
* { margin: 0; padding: 0; }
body { font-family: inherit; }

/* Global utilities */
.container { max-width: 1200px; }
.hidden { display: none; }
```

### Component Styles (`components/Button.css`)
```css
/* Button Component */
.btn { /* base styles */ }
.btn-primary { /* variant */ }
.btn-small { /* size */ }
.btn:hover { /* state */ }
```

### Page Styles (`Dashboard.css`)
```css
/* Dashboard Page */
.dashboard { /* page container */ }
.dashboard-header { /* header section */ }
.dashboard-content { /* content section */ }
```

### Animations (`Animations.css`)
```css
/* Animations Library */
@keyframes fadeIn { /* animation */ }
.fade-in { animation: fadeIn 0.6s ease-out; }
```

### Responsive (`ResponsiveMobile.css`)
```css
/* Mobile Responsive Styles */
@media (max-width: 768px) { /* tablet */ }
@media (max-width: 480px) { /* mobile */ }
```

## Component Hierarchy

```
App
├── Sidebar
├── Pages (Route-based)
│   ├── Login
│   ├── Dashboard
│   │   ├── StatCard (multiple)
│   │   ├── Card
│   │   └── Toast
│   ├── PostJob
│   │   ├── FormInput (multiple)
│   │   ├── Button
│   │   └── Toast
│   ├── UploadResume
│   │   ├── FormInput (multiple)
│   │   ├── Button
│   │   ├── LoadingSpinner
│   │   └── Toast
│   └── CandidateRanking
│       ├── Card
│       ├── Badge
│       ├── Button
│       └── Modal
└── ToastContainer
```

## Data Flow

### State Management
```
Page Component (useState)
├── Local state for form data
├── Local state for UI state
└── API calls via hooks
    └── useToast for notifications
```

### API Integration
```
Component
├── useEffect (fetch data)
├── API call (api.js)
├── Handle response
├── Update state
└── Render UI
```

### Props Flow
```
Page Component
├── Pass data to Card
├── Pass handlers to Button
├── Pass state to FormInput
└── Pass callbacks to Modal
```

## Best Practices

### 1. Component Design
- ✅ Single Responsibility Principle
- ✅ Reusable and composable
- ✅ Props-based configuration
- ✅ Proper error handling
- ✅ Loading states

### 2. CSS Organization
- ✅ Use CSS variables
- ✅ Mobile-first approach
- ✅ Consistent naming
- ✅ Avoid inline styles
- ✅ Responsive breakpoints

### 3. Code Quality
- ✅ JSDoc comments
- ✅ Meaningful variable names
- ✅ DRY principle
- ✅ Error handling
- ✅ Input validation

### 4. Performance
- ✅ Code splitting ready
- ✅ Lazy loading ready
- ✅ Optimized animations
- ✅ Efficient CSS
- ✅ Minimal re-renders

### 5. Accessibility
- ✅ Semantic HTML
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Color contrast
- ✅ Motion preferences

## Adding New Features

### Adding a New Component
1. Create file in `src/components/ComponentName.js`
2. Create styles in `src/styles/components/ComponentName.css`
3. Add JSDoc comments
4. Export default component
5. Import and use in pages

### Adding a New Page
1. Create file in `src/pages/PageName.js`
2. Create styles in `src/styles/PageName.css`
3. Import reusable components
4. Add to App.js routing
5. Update Sidebar navigation

### Adding New Styles
1. Create CSS file in appropriate directory
2. Use CSS variables
3. Include responsive breakpoints
4. Follow naming conventions
5. Import in component/page

## File Size Guidelines

| File Type | Max Size | Recommendation |
|-----------|----------|-----------------|
| Component | 300 lines | Split if larger |
| Page | 500 lines | Split if larger |
| CSS | 500 lines | Split if larger |
| Utility | 200 lines | Split if larger |

## Documentation Requirements

### Component Files
```javascript
/**
 * Component Name
 * Brief description of what it does
 * 
 * Usage:
 * <ComponentName prop1="value" prop2={value} />
 */
```

### Function Files
```javascript
/**
 * Function name
 * @param {type} paramName - Description
 * @returns {type} Description
 */
```

### CSS Files
```css
/* ============================================
   SECTION NAME
   ============================================ */
```

## Maintenance Checklist

- [ ] No duplicate code
- [ ] All components documented
- [ ] CSS organized by scope
- [ ] Responsive design tested
- [ ] Accessibility checked
- [ ] Performance optimized
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Comments added
- [ ] Naming conventions followed

## Summary

This organized structure ensures:
- ✅ Easy navigation and maintenance
- ✅ Scalability for new features
- ✅ Code reusability
- ✅ Team collaboration
- ✅ Production readiness
- ✅ Performance optimization
- ✅ Accessibility compliance
