// components/ui/Card.jsx
import React from "react";

const Card = ({ children, title }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      {title && <h2 className="text-lg font-bold mb-2">{title}</h2>}
      <div>{children}</div>
    </div>
  );
};

export const CardContent = ({ children }) => {
  return <div className="p-2">{children}</div>;
};

export default Card;
