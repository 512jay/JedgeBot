import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to JedgeBot</h1>
      <p>Manage your trading strategies with ease.</p>
      <div className="buttons">
        <Link to="/login" className="btn">Enter</Link>
      </div>
    </div>
  );
}

export default Home;
