import StatCard from '../../components/common/StatCard'

export default function DashboardPage() {
  return (
    <main className="section">
      <h2>Student Dashboard</h2>
      <div className="feature-grid">
        <StatCard label="Overall progress" value="0%" hint="Ready for backend wiring" />
        <StatCard label="Completed lessons" value="0" hint="No lessons unlocked yet" />
        <StatCard label="Certificates" value="0" hint="Module and course certificates" />
      </div>
    </main>
  )
}
