# Quick Start Guide - CodeGuard Frontend

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Create a `.env` file in the `frontend` directory:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Start Development Server
```bash
npm run dev
```

The app will open at `http://localhost:3000`

### 4. Make sure Backend is Running
The frontend needs the backend API to be running. In a separate terminal:

```bash
cd backend
# Activate virtual environment if needed
# source venv/bin/activate  # or your venv path
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎨 What You'll See

1. **Beautiful Landing Page** with hero section
2. **Code Editor** with syntax highlighting (Paste Code tab)
3. **File Upload** with drag & drop support (Upload File tab)
4. **Real-time Results** with similarity scores
5. **Risk Indicators** (High/Medium/Low)

## 📝 How to Use

### Method 1: Paste Code
1. Click "Paste Code" tab
2. Write or paste your Python code
3. Click "Check for Plagiarism"
4. View results in the right panel

### Method 2: Upload File
1. Click "Upload File" tab
2. Drag & drop or browse for a file
3. Supported: `.py`, `.txt`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
4. View results automatically

## 🎯 Features

- ✅ **Syntax Highlighting** - CodeMirror editor with Python support
- ✅ **Drag & Drop** - Easy file uploads
- ✅ **Real-time Feedback** - Toast notifications
- ✅ **Responsive Design** - Works on mobile and desktop
- ✅ **Beautiful UI** - Modern gradient backgrounds, smooth animations
- ✅ **Risk Assessment** - Color-coded similarity levels:
  - 🔴 Red (70%+): High Risk
  - 🟡 Yellow (40-69%): Medium Risk
  - 🟢 Green (<40%): Low Risk

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **CodeMirror 6** - Advanced code editor
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons
- **React Toastify** - Elegant notifications

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` folder.

To preview the production build:
```bash
npm run preview
```

## 🔧 Troubleshooting

### API Connection Issues
- Make sure backend is running on `http://localhost:8000`
- Check `.env` file has correct `VITE_API_BASE_URL`
- Open browser console to see network errors

### Port Already in Use
If port 3000 is busy, Vite will ask to use another port. Just accept it.

### Dependencies Not Installing
Try:
```bash
rm -rf node_modules package-lock.json
npm install
```

## 🎨 Customization

### Change Colors
Edit `frontend/tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      primary: {
        // Change these values
        500: '#0ea5e9',
        600: '#0284c7',
        // ...
      }
    }
  }
}
```

### Change API URL
Edit `.env`:
```
VITE_API_BASE_URL=https://your-api-domain.com/api/v1
```

## 📱 Screenshots Features

### Main Interface
- Split-screen design: Input on left, Results on right
- Tabbed interface: Paste Code / Upload File
- Professional gradient background

### Results Panel
- Clear success/warning indicators
- Detailed match information
- Direct links to source repositories
- Similarity percentage badges

## 🚢 Deployment

### Deploy to Netlify/Vercel
1. Build the project: `npm run build`
2. Deploy the `dist/` folder
3. Set environment variable: `VITE_API_BASE_URL=your-backend-url`

### Deploy with Docker
See main project README for Docker deployment instructions.

## 💡 Tips

1. **Use the code editor features**: Line numbers, syntax highlighting, bracket matching
2. **Check multiple files**: Upload different files to compare results
3. **Monitor similarity scores**: Higher percentages indicate more similarity
4. **Follow source links**: Click "View Source" to see original code

## 🆘 Need Help?

Check the main project README or open an issue on GitHub.

Enjoy using CodeGuard! 🎉

