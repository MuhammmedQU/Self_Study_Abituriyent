import { Link, Outlet } from 'react-router-dom'

export default function StudentLayout() {
  return (
    <div className="page-shell">
      <div className="container">
        <header className="navbar">
          <strong>LMS Student</strong>
          <nav className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/student/dashboard">Dashboard</Link>
            <Link to="/login">Login</Link>
          </nav>
        </header>
        <Outlet />
      </div>
    </div>
  )
}
