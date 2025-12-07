import { useState, useEffect } from "react";
import UploadBox from "./components/UploadBox";
import CameraFeed from "./components/CameraFeed";
import SecurityAlerts from "./components/SecurityAlerts";
import SurveillanceControl from "./components/SurveillanceControl";
import { getCameras, uploadSuspicious, getCameraStreamUrl } from "./api";

// ✅ Status cards inline
function StatusCards({ stats }) {
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

export default function App() {
  const [cameras, setCameras] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [matches, setMatches] = useState(0);

  useEffect(() => {
    getCameras().then((data) => setCameras(data.cameras || []));
  }, []);

  const handleUpload = async (file) => {
    const result = await uploadSuspicious(file);
    if (result.matches && result.matches.length > 0) {
      setMatches((prev) => prev + result.matches.length);
      setAlerts((prev) => [
        ...prev,
        {
          level: "HIGH",
          message: `Suspicious person detected with ${Math.round(
            (1 - result.matches[0].distance) * 100
          )}% confidence.`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-6 grid grid-cols-12 gap-6">
      {/* ✅ Top row status */}
      <div className="col-span-12">
        <StatusCards
          stats={[
            { label: "Active Cameras", value: `${cameras.length}/6` },
            { label: "Active Alerts", value: alerts.length },
            { label: "Scanning Status", value: "STANDBY" },
            { label: "Matches Found", value: matches },
          ]}
        />
      </div>

      {/* ✅ Left column */}
      <div className="col-span-3 space-y-6">
        <UploadBox onUpload={handleUpload} />
        <SurveillanceControl />
      </div>

      {/* ✅ Middle camera grid */}
      <div className="col-span-6 grid grid-cols-2 gap-4">
        {cameras.map((cam) => (
          <CameraFeed key={cam} camId={cam} url={getCameraStreamUrl(cam)} />
        ))}
      </div>

      {/* ✅ Alerts right */}
      <div className="col-span-3">
        <SecurityAlerts alerts={alerts} />
      </div>
    </div>
  );
}
// The main App component that integrates all parts of the Airport Surveillance System UI.