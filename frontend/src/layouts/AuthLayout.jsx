import { Link, Outlet } from 'react-router-dom'

export default function AuthLayout() {
  return (
    <div className="page-shell">
      <div className="container">
        <header className="navbar">
          <strong>LMS</strong>
          <div className="nav-links">
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </div>
        </header>
        <Outlet />
      </div>
    </div>
  )
}
