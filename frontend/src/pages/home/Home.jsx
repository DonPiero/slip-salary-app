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
    <div className="app-container">
      <div className="card">
        {isManager ? (
          <>
            <h1 className="center">Manager Dashboard</h1>
            <p className="muted center">
              You may use the actions below to manage your employees' salary slips:
            </p>

            <div className="actions">
              <button
                className="btn btn-primary"
                disabled={loading}
                onClick={() => handleAction("createAggregatedEmployeeData", "Create Excel file")}
              >
                Create Excel
              </button>
              <button
                className="btn btn-primary"
                disabled={loading}
                onClick={() => handleAction("createPdfForEmployees", "Create PDF files")}
              >
                Create PDF
              </button>
              <button
                className="btn btn-primary"
                disabled={loading}
                onClick={() => handleAction("sendAggregatedEmployeeData", "Send Excel file")}
              >
                Send Excel
              </button>
              <button
                className="btn btn-primary"
                disabled={loading}
                onClick={() => handleAction("sendPdfToEmployees", "Send PDF files")}
              >
                Send PDF
              </button>
            </div>

            {message && (
              <p
                className={`status ${
                  message.startsWith("Accomplished") ? "ok" : "error"
                } center`}
              >
                {message}
              </p>
            )}
          </>
        ) : (
          <>
            <h1 className="center">Employee Portal</h1>
            <h3 className="muted center">
              Hello, {user.email}! <br />
              Your manager will make sure your salary slip arrives by email as soon as possible, not later than the end of the month. <br />
              If you have any questions, please contact your HR department.
            </h3>
          </>
        )}

        <div className="logout">
          <button className="btn btn-danger" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
