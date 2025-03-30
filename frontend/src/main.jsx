// /frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import App from './features/app/App.jsx';
import { AuthProvider } from './context/AuthProvider.jsx';
import "./styles/global.css";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
