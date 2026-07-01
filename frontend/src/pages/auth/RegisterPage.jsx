import { useState } from 'react'

export default function RegisterPage() {
  const [form, setForm] = useState({ fullName: '', email: '', password: '' })
  return (
    <main className="section card-grid">
      <section className="card">
        <h2>Register</h2>
        <form className="form">
          <input placeholder="Full name" value={form.fullName} onChange={(event) => setForm({ ...form, fullName: event.target.value })} />
          <input placeholder="Email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
          <input type="password" placeholder="Password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
          <button className="btn btn-primary" type="button">Create account</button>
        </form>
      </section>
      <section className="card">
        <h3>Approval workflow</h3>
        <p style={{ color: 'var(--muted)', lineHeight: 1.7 }}>
          New accounts are pending until an administrator approves them.
        </p>
      </section>
    </main>
  )
}
