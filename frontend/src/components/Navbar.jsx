import { Link, useLocation, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleFeaturesClick = (e) => {
    e.preventDefault();
    navigate("/");

    setTimeout(() => {
      const section = document.getElementById("features");
      section?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        {/* 🔥 Home logo click */}
        <Link to="/" className="logo-link">
          <span className="logo">🎙️ PodcastAI</span>
        </Link>
      </div>

      <ul className="nav-links">
        {/* ✅ Home → Home.jsx */}
        <li className={location.pathname === "/" ? "active" : ""}>
          <Link to="/">Home</Link>
        </li>

        {/* ⭐ Features → Home.jsx + scroll */}
        <li>
          <Link to="/" onClick={handleFeaturesClick}>
            Features
          </Link>
        </li>

        {/* Other pages */}
        <li className={location.pathname === "/analytics" ? "active" : ""}>
          <Link to="/analytics">Analytics</Link>
        </li>

        <li className="nav-btn-highlight">
          <Link to="/insights">View Insights</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
