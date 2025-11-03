import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/home/Home.jsx";
import Login from "./pages/login/Login.jsx";

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login setUser={setUser} />} />
      <Route path="/" element={ user ? <Home user={user} setUser={setUser} /> : <Navigate to="/login" />}/>
    </Routes>
  );
}
