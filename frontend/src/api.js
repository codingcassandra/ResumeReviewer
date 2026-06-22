import axios from "axios";

export async function matchJob(resumeFile, jobText) {
  const formData = new FormData();

  formData.append("resume", resumeFile);
  formData.append("job_text", jobText);

  const response = await axios.post(
    "https://resumereviewer-fss9.onrender.com",
    formData
  );

  return response.data;
}