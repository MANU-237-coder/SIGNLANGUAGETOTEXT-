export async function sendFrame(blob) {
  const formData = new FormData();
  formData.append("frame", blob, "frame.jpg");

  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    throw new Error("Server error");
  }

  return await response.json();
}
