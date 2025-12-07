export default function SecurityAlerts({ alerts }) {
  return (
    <div className="bg-gray-900 p-4 rounded-xl border border-gray-700">
      <h2 className="text-white mb-4">Security Alerts</h2>
      <div className="space-y-3">
        {alerts.length === 0 && (
          <p className="text-gray-400 text-sm">No alerts</p>
        )}
        {alerts.map((alert, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg border ${
              alert.level === "HIGH" ? "border-red-500 bg-red-900/20" : "border-yellow-500 bg-yellow-900/20"
            }`}
          >
            <p className="text-white font-medium">{alert.message}</p>
            <p className="text-xs text-gray-400">{alert.timestamp}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
// A component to display security alerts with severity levels.