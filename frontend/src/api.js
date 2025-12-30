// src/api.js
export const uploadAudio = async (file, mode) => {
  const formData = new FormData();
  formData.append("audio", file);
  formData.append("mode", mode);

  const response = await fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || "Server error");
  }
  return response.json();
};