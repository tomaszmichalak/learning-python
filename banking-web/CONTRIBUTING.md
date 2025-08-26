# Contributing to Banking Web Application 🚀

Welcome to the Banking Web Application! This guide will help you set up your development environment, understand the project structure, and contribute effectively.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Debugging Guide](#debugging-guide)
- [WebSocket Development](#websocket-development)
- [Testing](#testing)
- [Building and Deployment](#building-and-deployment)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- **Node.js 20.x or higher**
- **npm or yarn package manager**
- **Banking API running on http://localhost:8000**
- **VS Code with recommended extensions**:
  - TypeScript and JavaScript Language Features
  - JavaScript Debugger
  - ES6 Mocha Snippets (optional)
  - Auto Rename Tag (optional)

### Installation

1. Navigate to the banking-web directory
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at http://localhost:5173

## Development Setup

### VS Code Configuration

This project includes comprehensive VS Code debugging support with pre-configured launch configurations:

- **🚀 Debug Full Stack (API + Web)** - Debug both applications simultaneously
- **⚛️ Debug Banking Web - Chrome** - Debug React app in Chrome
- **🌐 Debug Banking Web - Dev Server** - Debug the Vite dev server
- **🔨 Debug Banking Web - Build** - Debug build process
- **📱 Debug Banking Web - Edge** - Debug React app in Edge

### Environment Setup

For local debugging, stop the Docker container:
```bash
cd /Users/tomaszmichalak/Projects/learning-python/banking-compose
docker compose down banking-web
```

## Project Structure

```
banking-web/
├── src/
│   ├── components/
│   │   ├── TransactionStream.tsx      # Main transaction stream component
│   │   └── TransactionStream.css      # Component styles
│   ├── hooks/
│   │   └── useWebSocket.ts            # WebSocket hook with reconnection
│   ├── types/
│   │   └── transaction.ts             # TypeScript type definitions
│   ├── App.tsx                        # Main application component
│   ├── App.css                        # Application styles
│   ├── main.tsx                       # Application entry point
│   └── index.css                      # Global styles
├── public/                            # Public assets (currently empty)
├── index.html                         # Main HTML file
├── package.json                       # Node.js dependencies
├── tsconfig.json                      # TypeScript configuration
├── vite.config.ts                     # Vite build configuration
└── README.md
```

## Development Workflow

### Starting Development

1. **Quick Start Debugging**:
   - Open VS Code Debug panel (`Cmd+Shift+D`)
   - Select **"🚀 Debug Full Stack (API + Web)"**
   - Click the green play button ▶️

2. **Manual Setup**:
   ```bash
   # Start development server
   npm run dev
   
   # In another terminal, ensure banking API is running
   # The app will be available at http://localhost:5173
   ```

### Setting Breakpoints

#### Frontend (TypeScript) Breakpoints:
```typescript
// File: src/components/TransactionStream.tsx
const TransactionStream: React.FC<TransactionStreamProps> = ({ accountId }) => {
  // 🐛 SET BREAKPOINT HERE
  const { isConnected, error, lastMessage } = useWebSocket(wsUrl);
```

#### WebSocket Hook Breakpoints:
```typescript
// File: src/hooks/useWebSocket.ts
export const useWebSocket = (url: string): UseWebSocketReturn => {
  // 🐛 SET BREAKPOINT HERE for connection debugging
  const connect = useCallback(() => {
    ws.current = new WebSocket(url);
    
    ws.current.onmessage = (event) => {
      // 🐛 SET BREAKPOINT HERE for message handling
      const data = JSON.parse(event.data);
    };
  }, [url]);
};
```

## Debugging Guide

### Available Debug Methods

#### Method 1: Debug Dev Server (Recommended)

1. Navigate to banking-web in VS Code explorer
2. Set breakpoints in React components
3. Press `F5` and select "Debug Banking Web - Dev Server"
4. Open browser at http://localhost:5173

#### Method 2: Debug in Chrome

1. Start dev server manually:
   ```bash
   npm run dev
   ```
2. Press `F5` and select "Debug Banking Web - Chrome"
3. Chrome launches with debugging enabled

#### Method 3: Attach to Running Chrome

1. Start Chrome with remote debugging:
   ```bash
   # macOS
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
   ```
2. Navigate to http://localhost:5173
3. Press `F5` and select "Debug Banking Web - Attach Chrome"

### Common Debugging Scenarios

#### Debugging React Components

Set breakpoints in:
- Component render methods
- useEffect hooks
- Event handlers
- State updates

#### Debugging WebSocket Connections

Key debugging points:
1. **Connection establishment**
2. **Message parsing**
3. **State updates**
4. **Error handling**
5. **Reconnection logic**

Debug workflow:
```bash
# 1. Start both applications in debug mode
# 2. Set breakpoints in both frontend and backend
# 3. Create test transaction:
curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"account_id": "test-id", "amount": 100, "transaction_type": "deposit", "description": "Debug test"}'
```

## WebSocket Development

### Architecture

The application uses WebSocket connections for real-time transaction updates:

- **TransactionStream** - Main component with account filtering
- **useWebSocket** - Robust WebSocket hook with automatic reconnection

### WebSocket Message Flow

```
1. User action in React app
2. HTTP request to banking-api
3. API processes transaction
4. WebSocket broadcast from API
5. Message received in React hook
6. Component state updated
7. UI re-renders with new data
```

### Testing WebSocket Functionality

#### Manual Testing

1. Start both applications (API on port 8000, Web on port 5173)
2. Open browser console to see WebSocket logs
3. Create test data:
   ```bash
   # Create account
   account_id=$(curl -s -X POST http://localhost:8000/api/accounts \
     -H "Content-Type: application/json" \
     -d '{"account_holder": "Test User", "account_type": "checking", "initial_balance": 1000}' \
     | jq -r '.account_id')

   # Create transaction (should appear in real-time)
   curl -X POST http://localhost:8000/api/transactions \
     -H "Content-Type: application/json" \
     -d "{\"account_id\": \"$account_id\", \"amount\": 100, \"transaction_type\": \"deposit\", \"description\": \"Test transaction\"}"
   ```

## Testing

### Manual Testing Checklist

- [ ] WebSocket connection establishes successfully
- [ ] Real-time transaction updates appear
- [ ] Account filtering works correctly
- [ ] Error handling works (disconnect/reconnect)
- [ ] UI responds to state changes
- [ ] No memory leaks in long-running sessions

## Building and Deployment

### Development Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Docker Build

```bash
cd /Users/tomaszmichalak/Projects/learning-python/banking-compose
docker compose build banking-web
```

### Scripts Available

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## Troubleshooting

### Common Issues

#### 1. Breakpoints Not Hitting
- ✅ Ensure source maps are enabled
- ✅ Check that dev server is running with debugging
- ✅ Verify TypeScript compilation is successful

#### 2. WebSocket Connection Fails
- ✅ Check banking-api is running on port 8000
- ✅ Verify CORS configuration
- ✅ Check WebSocket URL in browser console
- ✅ Ensure correct URL: `ws://localhost:3000/api/ws/transactions` (via proxy)

#### 3. Hot Reload Not Working
- ✅ Restart Vite dev server
- ✅ Check for TypeScript errors
- ✅ Clear browser cache

#### 4. Build Fails
- ✅ Run `npm run build` to see errors
- ✅ Check TypeScript configuration
- ✅ Verify all imports are correct

### Debug Console Commands

Use these in VS Code debug console:
```javascript
// Check WebSocket state
ws.current?.readyState

// Inspect transactions
transactions.length

// Check connection status
isConnected

// Force re-render
setTransactions([])
```

### Production Debugging

1. Use "Debug Banking Web - Vite Build" configuration
2. Check build output in `dist/` folder
3. Verify production WebSocket connections

## API Integration

### Endpoints Used

- `GET /api/accounts` - Fetches all banking accounts
- `GET /api/transactions` - Fetches transactions
- `POST /api/transactions` - Creates new transactions
- `WebSocket /api/ws/transactions` - Real-time transaction updates

### Full-Stack Debugging

1. Start both applications in debug mode
2. Set breakpoints in both frontend and backend
3. Test end-to-end transaction flow
4. Debug WebSocket message broadcasting

## Technologies Used

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool with debugging support
- **WebSocket API** - Real-time communication
- **CSS3** - Modern styling with Grid and Flexbox

## Development Tools

### Debugging Features
- VS Code debug configurations for full-stack debugging
- Chrome/Edge debugging support
- Source maps for TypeScript debugging

### WebSocket Features
- Real-time connection status monitoring
- Automatic reconnection with exponential backoff
- Error handling and user feedback
- Account-filtered transaction streams

## Contributing Guidelines

1. **Fork the repository** and create a feature branch
2. **Follow TypeScript best practices** and maintain type safety
3. **Add comprehensive error handling** for all WebSocket operations
4. **Write meaningful commit messages** following conventional commits
5. **Test thoroughly** including WebSocket edge cases
6. **Update documentation** for any new features or changes

---

Happy coding! 🎉⚛️

For questions or issues, please refer to the troubleshooting section or create an issue in the repository.
