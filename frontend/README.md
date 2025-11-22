# CodeGuard Frontend

A beautiful, modern React application for code plagiarism detection powered by AI.

## Features

- 🎨 **Beautiful UI** - Modern design with Tailwind CSS
- 📝 **Code Editor** - Syntax highlighting with CodeMirror
- 📤 **File Upload** - Drag and drop file support
- ⚡ **Real-time Analysis** - Fast plagiarism detection
- 🎯 **Detailed Results** - Comprehensive similarity reports
- 📱 **Responsive** - Works on all devices

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **CodeMirror** - Code editor
- **Axios** - API requests
- **Lucide React** - Icons
- **React Toastify** - Notifications

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update the API URL in `.env` if needed:
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Usage

### Paste Code
1. Click on the "Paste Code" tab
2. Enter or paste your code in the editor
3. Click "Check for Plagiarism"
4. View results on the right panel

### Upload File
1. Click on the "Upload File" tab
2. Drag and drop a file or click to browse
3. Supported formats: .py, .txt, .js, .java, .cpp, .c, .go, .rs
4. View results on the right panel

## API Integration

The frontend communicates with the backend API at `/api/v1`:

- `POST /api/v1/check` - Check code for plagiarism
- `POST /api/v1/upload` - Upload file for plagiarism check
- `GET /api/v1/health` - Health check

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── CodeInput.jsx
│   │   └── Results.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Color Scheme

The application uses a modern blue color palette:

- **Primary**: Blue (#0ea5e9)
- **Success**: Green
- **Warning**: Yellow
- **Danger**: Red

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT

