export default function SurveillanceControl() {
  return (
    <div className="bg-gray-900 p-4 rounded-xl border border-gray-700">
      <h2 className="text-white mb-4">Surveillance Control</h2>
      <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white">
        Start Surveillance
      </button>

      <div className="mt-4">
        <label className="text-gray-300 text-sm">Confidence Threshold</label>
        <input type="range" min="50" max="100" defaultValue="75" className="w-full mt-2" />
      </div>

      <div className="flex justify-between text-gray-400 text-xs mt-4">
        <span>Active Cameras: 5/6</span>
        <span>System Active</span>
      </div>
    </div>
  );
}
// A control panel for managing surveillance settings and status.