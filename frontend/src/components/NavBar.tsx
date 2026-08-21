import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <header className="navbar">
      <Link to="/" className="brand">
        BiblioTech
      </Link>
      <nav className="nav-links">
        <Link to="/">Catalog</Link>
        {user && <Link to="/cart">Cart</Link>}
        {user && <Link to="/wishlist">Wishlist</Link>}
        {user && <Link to="/profile">Profile</Link>}
        {user?.is_admin && <Link to="/admin">Admin</Link>}
      </nav>
      <div className="nav-auth">
        {user ? (
          <>
            <span className="nav-username">{user.username}</span>
            <button className="btn btn-ghost" onClick={handleLogout}>
              Log out
            </button>
          </>
        ) : (
          <>
            <Link className="btn btn-ghost" to="/login">
              Log in
            </Link>
            <Link className="btn btn-primary" to="/register">
              Sign up
            </Link>
          </>
        )}
      </div>
    </header>
  );
}
