// /frontend/src/features/app/App.jsx
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AppRoutes from "@/routes/AppRoutes";

function App() {
  return (
    <>
      <ToastContainer position="top-center" autoClose={4000} />
      <AppRoutes />
    </>
  );
}

export default App;
