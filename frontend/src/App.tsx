import { useState } from "react";

function App() {
  const [healthStatus, setHealthStatus] = useState<string | null>(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [a, setA] = useState<string>("");
  const [b, setB] = useState<string>("");
  const [sumResult, setSumResult] = useState<string | null>(null);
  const [sumLoading, setSumLoading] = useState(false);
  const [sumError, setSumError] = useState<string | null>(null);

  const API_BASE = "http://127.0.0.1:8000";

  const checkHealth = async () => {
    try {
      setHealthLoading(true);
      setHealthError(null);
      const res = await fetch(`${API_BASE}/health`);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();
      setHealthStatus(JSON.stringify(data));
    } catch (err: any) {
      setHealthError(err.message ?? "Unknown error");
    } finally {
      setHealthLoading(false);
    }
  };

  const calcSum = async () => {
    if (a.trim() === "" || b.trim() === "") {
      setSumError("Both a and b are required");
      setSumResult(null);
      return;
    }

    if (Number.isNaN(Number(a)) || Number.isNaN(Number(b))) {
      setSumError("a and b must be numbers");
      setSumResult(null);
      return;
    }

    try {
      setSumLoading(true);
      setSumError(null);
      setSumResult(null);

      const params = new URLSearchParams({ a, b });
      const res = await fetch(`${API_BASE}/calc/sum?${params.toString()}`);

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        const msg = data?.detail ?? `HTTP ${res.status}`;
        throw new Error(msg);
      }

      const data = await res.json();
      setSumResult(String(data.result));
    } catch (err: any) {
      setSumError(err.message ?? "Unknown error");
    } finally {
      setSumLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "system-ui", maxWidth: 600 }}>
      <h1>Fullstack Lab</h1>

      {/* Health check section */}
      <section style={{ marginBottom: "2rem" }}>
        <h2>API Health</h2>
        <button onClick={checkHealth} disabled={healthLoading}>
          {healthLoading ? "Checking..." : "Check API health"}
        </button>
        {healthStatus && <p>API response: {healthStatus}</p>}
        {healthError && <p style={{ color: "red" }}>Error: {healthError}</p>}
      </section>

      {/* Calculator section */}
      <section>
        <h2>Sum Calculator (/calc/sum)</h2>
        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
          <input
            type="text"
            placeholder="a"
            value={a}
            onChange={(e) => setA(e.target.value)}
          />
          <input
            type="text"
            placeholder="b"
            value={b}
            onChange={(e) => setB(e.target.value)}
          />
          <button onClick={calcSum} disabled={sumLoading}>
            {sumLoading ? "Calculating..." : "Calculate"}
          </button>
        </div>

        {sumResult !== null && <p>Result: {sumResult}</p>}
        {sumError && <p style={{ color: "red" }}>Error: {sumError}</p>}
      </section>
    </div>
  );
}

export default App;
