import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!resume) {
      alert("Please upload a resume.");
      return;
    }

    if (!jobText.trim()) {
      alert("Please paste a job description.");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_text", jobText.trim());

    try {
      const response = await axios.post(
        "https://resumereviewer-fss9.onrender.com/match-job",
        formData
      );

      console.log("FULL BACKEND RESPONSE:", response.data);

      const data = response.data;

      const matchData = data?.match || data?.analysis || data?.result;

      if (!matchData) {
        console.log("Invalid backend response:", data);
        alert("Backend did not return usable match data. Check console.");
        return;
      }

      setResult(matchData);

    } catch (error) {
      console.log("FULL ERROR:", error);
      alert("Backend error — check console");
    } finally {
      setLoading(false);
    }
  }

  function getScore(r) {
    return (
      r?.match_score ??
      r?.overall_match_score ??
      r?.score ??
      0
    );
  }

  function getVerdictClass(verdict) {
    if (!verdict) return "";

    const v = verdict.toLowerCase();

    if (v.includes("strong")) return "strong";
    if (v.includes("moderate")) return "moderate";
    if (v.includes("weak")) return "weak";

    return "";
  }

  return (
    <div className="app-wrapper">
      <div className="container">
        <h1>AI Resume Reviewer</h1>

        <input
          type="file"
          onChange={(e) => setResume(e.target.files[0])}
        />

        <textarea
          rows="10"
          placeholder="Paste job description here..."
          value={jobText}
          onChange={(e) => setJobText(e.target.value)}
        />

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {result && (
          <div className="results">

            <h2 className="score">
              Match Score: {getScore(result)}%
            </h2>

            <h3 className={`verdict ${getVerdictClass(result.verdict)}`}>
              {result?.verdict || "Analysis Complete"}
            </h3>

            <h3>Matched Skills</h3>
            <div className="skills">
              {(result?.matched_skills || []).map((skill, i) => (
                <span key={i} className="skill">
                  {skill}
                </span>
              ))}
            </div>

            <h3>Recommendation</h3>
            <p>{result?.recommendation || "N/A"}</p>

          </div>
        )}
      </div>
    </div>
  );
}

export default App;