// /frontend/src/components/common/ToastMessage.jsx
// Reusable toast message using native Bootstrap 5 classes

import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const ToastMessage = ({
  show,
  message,
  type = "info", // success, danger, warning, info
  delay = 30000,
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

  const bgColor = {
    success: "bg-success text-white",
    danger: "bg-danger text-white",
    warning: "bg-warning text-dark",
    info: "bg-info text-white",
  }[type];

  return (
    <div
      className="position-fixed top-0 end-0 p-3"
      style={{ zIndex: 9999, maxWidth: "300px" }}
    >
      <div
        className={`toast show ${bgColor}`}
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div className="toast-header">
          <strong className="me-auto">JedgeBot</strong>
          <button
            type="button"
            className="btn-close"
            aria-label="Close"
            onClick={() => {
              setVisible(false);
              onClose();
            }}
          ></button>
        </div>
        <div className="toast-body">{message}</div>
      </div>
    </div>
  );
};

export default ToastMessage;
