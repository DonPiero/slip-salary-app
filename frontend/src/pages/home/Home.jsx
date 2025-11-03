import { useState } from "react";

export default function Home({ user, setUser }) {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const handleLogout = () => {
        setUser(null);
        localStorage.removeItem("user");
    };

    const isManager = user.role === "manager";

  async function handleAction(endpoint, label) {
      setLoading(true);
    setMessage(`Running: ${label}...`);

    try {
      const response = await fetch(`http://localhost:8000/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
      });

      if (!response.ok) {
        const err = await response.text();
        setMessage(`${label} failed: ${err}.`);
        setLoading(false);
        return;
      }

      setMessage(`Accomplished! ${label} completed successfully.`);
    } catch (err) {
      console.error(err);
      setMessage(`${label} failed: ${err}.`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      {isManager ? (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Manager Dashboard</h3>
          <p>You can use the actions below to manage salary slips:</p>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "0.5rem",
              marginTop: "1rem",
            }}
          >
            <button disabled={loading}
              onClick={() => handleAction("createAggregatedEmployeeData", "Create Excel file")}>
              Create Excel
            </button>
            <button disabled={loading}
              onClick={() => handleAction("createPdfForEmployees", "Create PDF files")}>
              Create PDF
            </button>
            <button disabled={loading}
              onClick={() => handleAction("sendAggregatedEmployeeData", "Send Excel file")}>
              Send Excel
            </button>
            <button disabled={loading}
              onClick={() => handleAction("sendPdfToEmployees", "Send PDF files")}>
              Send PDF
            </button>
          </div>
          {message && (
            <p
              style={{
                marginTop: "1rem",
                fontWeight: "bold",
                color: message.startsWith("Accomplished")
                  ? "green"
                  : "red"
              }}
            >
              {message}
            </p>
          )}
        </div>
      ) : (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Employee Portal</h3>
          <p>Hello, {user.email}! <br/>
             Your manager will make sure your salary slip arrives by email.</p>
        </div>
      )}

      <div style={{ marginTop: "2rem" }}>
        <button onClick={handleLogout} style={{ padding: "0.5rem 1rem" }}>
          Logout
        </button>
      </div>
    </div>
  );
}
