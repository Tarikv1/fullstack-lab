import { useEffect, useState } from "react";
import { fetchNotes, createNote, deleteNote, type Note } from "./api";

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadNotes() {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchNotes();
      setNotes(data);
    } catch (e) {
      setError("Failed to load notes");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadNotes();
  }, []);

  async function handleAddNote(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() && !content.trim()) return;

    try {
      setSaving(true);
      setError(null);
      const newNote = await createNote({ title, content });
      setNotes((prev) => [newNote, ...prev]);
      setTitle("");
      setContent("");
    } catch (e: any) {
      console.error("Save note error:", e?.response?.data || e);
      setError("Failed to save note");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteNote(id);
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch (e) {
      setError("Failed to delete note");
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: "2rem" }}>
      <h1>Notes</h1>

      <form onSubmit={handleAddNote} style={{ marginBottom: "1.5rem" }}>
        <div style={{ marginBottom: "0.5rem" }}>
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <div style={{ marginBottom: "0.5rem" }}>
          <textarea
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={4}
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <button type="submit" disabled={saving}>
          {saving ? "Saving..." : "Add Note"}
        </button>
      </form>

      {loading && <p>Loading notes...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {notes.map((note) => (
          <li
            key={note.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: "0.75rem 1rem",
              marginBottom: "0.75rem",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <h3 style={{ margin: 0 }}>{note.title || "Untitled"}</h3>
              <button onClick={() => handleDelete(note.id)}>Delete</button>
            </div>
            {note.content && <p style={{ marginTop: "0.5rem" }}>{note.content}</p>}
            {note.created_at && (
              <small style={{ color: "#666" }}>
                {new Date(note.created_at).toLocaleString()}
              </small>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
