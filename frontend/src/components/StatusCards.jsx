export default function StatusCards({ stats }) {
  return (
    <div className="grid grid-cols-4 gap-4 mb-6">
      {stats.map((s, i) => (
        <div
          key={i}
          className="bg-gray-900 p-4 rounded-xl border border-gray-700 text-center"
        >
          <h3 className="text-gray-400 text-sm">{s.label}</h3>
          <p className="text-white text-xl font-bold mt-2">{s.value}</p>
        </div>
      ))}
    </div>
  );
}
// A component to display status cards with various statistics.