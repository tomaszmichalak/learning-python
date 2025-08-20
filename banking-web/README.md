# Banking Web Application

A React TypeScript frontend application for displaying banking accounts from the banking API.

## Features

- Display all banking accounts in a responsive grid layout
- Show account details including owner name, account number, type, and balance
- Real-time account balance formatting with currency display
- Dark/light mode support
- Error handling with retry functionality
- Loading states for better user experience

## Prerequisites

- Node.js 20.x or higher
- npm or yarn package manager
- Banking API running on http://localhost:8000

## Installation

1. Clone the repository or navigate to the banking-web directory
2. Install dependencies:
   ```bash
   npm install
   ```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Building for Production

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## API Integration

The application connects to the banking API at `http://localhost:8000/accounts`. Make sure the banking API is running before starting this frontend application.

### API Endpoints Used

- `GET /accounts` - Fetches all banking accounts

## Project Structure

```
src/
├── App.tsx          # Main application component
├── App.css          # Application styles
├── main.tsx         # Application entry point
└── index.css        # Global styles
```

## Technologies Used

- React 18
- TypeScript
- Vite
- CSS3 with CSS Grid and Flexbox
- Fetch API for HTTP requests

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## CORS Configuration

If you encounter CORS issues, make sure the banking API includes the appropriate CORS headers to allow requests from http://localhost:3000.
