import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx';
import "./styles/global.css";


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>,
)
