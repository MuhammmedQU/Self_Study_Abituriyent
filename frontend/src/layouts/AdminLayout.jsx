import { Link, Outlet } from 'react-router-dom'

export default function AdminLayout() {
  return (
    <div className="page-shell">
      <div className="container">
        <header className="navbar">
          <strong>LMS Admin</strong>
          <nav className="nav-links">
            <Link to="/admin">Dashboard</Link>
            <Link to="/">Public Site</Link>
          </nav>
        </header>
        <Outlet />
      </div>
    </div>
  )
}
