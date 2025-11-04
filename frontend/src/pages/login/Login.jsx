import { useState } from "react";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
  e.preventDefault();
  setError("");

  try {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      setError("Invalid email or password. Please try again.");
      return;
    }

    const data = await response.json();
    const userData = {
        email,
        role: data.role,
        token: data.access_token,
      };

    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  } catch (err) {
    console.error(err);
    setError("There is an error with the server. Please try again later.");
  }
}


  return (
    <div className="app-container">
      <div className="card">
        <h1 className="center">Connect to your account</h1>
        <form className="form" onSubmit={handleSubmit}>
          <input
            className="input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="status error">{error}</p>}

          <button className="btn btn-primary" type="submit">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
