export default function UploadBox({ onUpload }) {
  return (
    <div className="p-4 bg-gray-900 rounded-xl border border-gray-700 text-center">
      <h2 className="text-white mb-2">Suspicious Person Upload</h2>
      <input
        type="file"
        accept="image/*"
        className="hidden"
        id="fileInput"
        onChange={(e) => onUpload(e.target.files[0])}
      />
      <label
        htmlFor="fileInput"
        className="block p-6 border-2 border-dashed border-gray-600 rounded-lg cursor-pointer text-gray-400 hover:border-blue-500 hover:text-white"
      >
        Drop photo here or click to upload
      </label>
    </div>
  );
}
// A simple upload box component for uploading images of suspicious persons.