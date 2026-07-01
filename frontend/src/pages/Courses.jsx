import React, { useEffect, useState } from "react";
import api from "../services/api";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const res = await api.get("/student/courses");
      setCourses(res.data.data);
    } catch (err) {
      console.error("Failed to fetch courses", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={{ padding: "20px" }}>Loading...</div>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Courses</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: "20px" }}>
        {courses.map((course) => (
          <div key={course.id} style={{ border: "1px solid #ddd", padding: "15px", borderRadius: "5px" }}>
            <h3>{course.title}</h3>
            <p>{course.description}</p>
            <button style={{ padding: "8px 16px", background: "#007bff", color: "white", border: "none", cursor: "pointer" }}>
              Enroll
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
