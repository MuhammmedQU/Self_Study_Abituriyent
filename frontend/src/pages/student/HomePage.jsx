import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <main className="hero">
      <div className="hero-grid">
        <section>
          <span className="kicker">Clean Architecture LMS</span>
          <h1>Build, manage, and track learning in one place.</h1>
          <p>
            This starter follows the prompt's core structure: FastAPI backend, React frontend, local file storage,
            role-based routing, and a clean foundation for courses, modules, lessons, quizzes, and certificates.
          </p>
          <div className="actions">
            <Link className="btn btn-primary" to="/register">Start learning</Link>
            <Link className="btn btn-secondary" to="/login">Admin login</Link>
          </div>
        </section>
        <aside className="panel glass sidebar">
          <div className="metric-grid">
            <div className="metric"><strong>14</strong><div>Planned steps</div></div>
            <div className="metric"><strong>FastAPI</strong><div>Backend</div></div>
            <div className="metric"><strong>React</strong><div>Frontend</div></div>
          </div>
          <div className="card">
            <h3>What is included now</h3>
            <p style={{ color: 'var(--muted)', lineHeight: 1.7 }}>
              Project scaffolding, backend entrypoint, local storage abstraction, initial SQLAlchemy models, and a modern frontend shell.
            </p>
          </div>
        </aside>
      </div>
    </main>
  )
}
