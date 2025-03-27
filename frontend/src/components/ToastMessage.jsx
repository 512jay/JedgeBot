// /frontend/src/components/ui/ToastMessage.jsx
// Reusable toast-like alert component using MDB React UI Kit

import React, { useEffect, useState } from "react";
import { MDBAlert } from "mdb-react-ui-kit";

const ToastMessage = ({
  show,
  message,
  type = "info", // "success", "danger", "warning", "info"
  delay = 4000,
  onClose = () => {},
}) => {
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    if (show) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
        onClose();
      }, delay);
      return () => clearTimeout(timer);
    }
  }, [show, delay, onClose]);

  if (!visible) return null;

  return (
    <div
      className="position-fixed top-0 end-0 p-3"
      style={{ zIndex: 9999, maxWidth: "300px" }}
    >
      <MDBAlert color={type} className="mb-0 text-white">
        {message}
      </MDBAlert>
    </div>
  );
};

export default ToastMessage;
