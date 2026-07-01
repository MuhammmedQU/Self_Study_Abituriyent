export default function StatCard({ label, value, hint }) {
  return (
    <div className="metric">
      <strong>{value}</strong>
      <div>{label}</div>
      <small style={{ color: 'var(--muted)' }}>{hint}</small>
    </div>
  )
}
