export default function CameraFeed({ camId, url }) {
  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden relative">
      <img
        src={url}
        alt={`Camera ${camId}`}
        className="w-full h-48 object-cover"
      />
      <div className="absolute top-1 left-1 bg-green-500 text-xs text-white px-2 py-1 rounded">
        {camId.toUpperCase()}
      </div>
    </div>
  );
}
// A component to display a single camera feed with its ID.