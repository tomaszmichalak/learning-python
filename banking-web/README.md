# Banking Web Application

A React TypeScript frontend application for displaying banking accounts and real-time transaction updates.

## Features

- Display all banking accounts in a responsive grid layout
- Show account details including owner name, account number, type, and balance
- **Real-time transaction updates via WebSocket**
- **Live transaction streaming with account filtering**
- Real-time account balance formatting with currency display
- Dark/light mode support
- Error handling with retry functionality
- Loading states for better user experience

## Prerequisites

- Node.js 20.x or higher
- npm or yarn package manager
- Banking API running on http://localhost:8000

## Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at http://localhost:5173

## WebSocket Features 🔄

Real-time transaction updates:
- **TransactionStream** - Live transaction updates with WebSocket connection
- **useWebSocket** - Robust WebSocket hook with automatic reconnection

## API Integration

The application connects to the banking API at `http://localhost:8000`. 

### API Endpoints
- `GET /api/accounts` - Fetches all banking accounts
- `GET /api/transactions` - Fetches transactions  
- `POST /api/transactions` - Creates new transactions
- `WebSocket /api/ws/transactions` - Real-time transaction updates

## Technologies Used

- React 18 with TypeScript
- Vite build tool
- WebSocket API for real-time updates
- CSS3 with responsive design

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production  
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Building for Production

```bash
npm run build
npm run preview
```

## Contributing

For development setup, debugging, and contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is part of the learning-python repository.
