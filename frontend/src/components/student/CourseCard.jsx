export default function CourseCard({ title, description }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <p style={{ color: 'var(--muted)', lineHeight: 1.7 }}>{description}</p>
    </article>
  )
}