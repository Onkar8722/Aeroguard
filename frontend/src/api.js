const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function getCameras() {
  try {
    const res = await fetch(`${API_BASE}/cameras`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return res.json();
  } catch (error) {
    console.error("Error fetching cameras:", error);
    return { cameras: [] };
  }
}

export async function uploadSuspicious(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}/upload_suspicious`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return res.json();
  } catch (error) {
    console.error("Error uploading suspicious image:", error);
    return { matches: [], error: error.message };
  }
}

export function getCameraStreamUrl(camId) {
  return `${API_BASE}/stream/${camId}`;
}