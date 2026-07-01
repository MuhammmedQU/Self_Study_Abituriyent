import { useState } from 'react'

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' })
  return (
    <main className="section card-grid">
      <section className="card">
        <h2>Login</h2>
        <form className="form">
          <input placeholder="Email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          <input type="password" placeholder="Password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
          <button className="btn btn-primary" type="button">Sign in</button>
        </form>
      </section>
      <section className="card">
        <h3>Secure authentication</h3>
        <p style={{ color: 'var(--muted)', lineHeight: 1.7 }}>
          This view is wired for the access + refresh token flow described in the specification.
        </p>
      </section>
    </main>
  )
}
