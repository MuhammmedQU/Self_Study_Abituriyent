export default function ConfirmDeleteModal({ title, children }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p style={{ color: 'var(--muted)' }}>{children}</p>
    </div>
  )
}