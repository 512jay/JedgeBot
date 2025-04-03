// /frontend/src/components/ui/Card.jsx
const Card = ({ children, className }) => {
  return <div data-testid="card" className={`bg-white rounded-lg shadow-lg ${className || ""}`}>{children}</div>;
};

const CardContent = ({ children, className }) => {
  return <div data-testid="card-content" className={`p-6 ${className || ""}`}>{children}</div>;
};


export { Card, CardContent };
