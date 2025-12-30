import axios from "axios";

export async function uploadAudio(file) {
  const formData = new FormData();
  formData.append("audio", file);

  const res = await axios.post(
    "http://127.0.0.1:5000/upload",
    formData
  );

  return res.data;
}
