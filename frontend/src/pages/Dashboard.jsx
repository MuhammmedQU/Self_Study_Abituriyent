import React, { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [progress, setProgress] = useState([]);

  useEffect(() => {
    fetchProgress();
  }, []);

  const fetchProgress = async () => {
    try {
      const res = await api.get("/student/progress/1");
      setProgress(res.data.data);
    } catch (err) {
      console.error("Failed to fetch progress", err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Welcome {user?.email}</h1>
      <button onClick={logout} style={{ padding: "10px", background: "#dc3545", color: "white", border: "none", cursor: "pointer" }}>
        Logout
      </button>
      <h2>Your Progress</h2>
      <div style={{ marginTop: "20px" }}>
        {progress.length === 0 ? (
          <p>No progress yet. Start learning!</p>
        ) : (
          <ul>
            {progress.map((p) => (
              <li key={p.module_id}>
                Module {p.module_id}: {p.completed} lessons completed
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
