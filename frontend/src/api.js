const API_BASE = "http://127.0.0.1:8000";  // backend

export async function getCameras() {
  const res = await fetch(`${API_BASE}/cameras`);
  return res.json();
}

export async function uploadSuspicious(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/upload_suspicious`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export function getCameraStreamUrl(camId) {
  return `${API_BASE}/stream/${camId}`;
}
// This file contains functions to interact with the backend API for camera management and face recognition.