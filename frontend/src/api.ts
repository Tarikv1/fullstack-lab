import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
});

export type Note = {
  id: number;
  title: string;
  content: string;
  created_at?: string;
};

// GET /notes
export async function fetchNotes(): Promise<Note[]> {
  const res = await api.get("/notes");
  return res.data.map((n: any) => ({
    id: n.id,
    title: n.title,
    content: n.content ?? n.body ?? "",
    created_at: n.created_at,
  }));
}

// POST /notes
export async function createNote(data: { title: string; content: string }) {
  const res = await api.post("/notes", {
    title: data.title,
    body: data.content, // backend expects "body"
  });

  const n = res.data;
  return {
    id: n.id,
    title: n.title,
    content: n.content ?? n.body ?? "",
    created_at: n.created_at,
  } as Note;
}

// “Update” note = create new + delete old (no backend PUT needed)
export async function updateNote(
  oldId: number,
  data: { title: string; content: string }
) {
  const newNote = await createNote(data);
  await deleteNote(oldId);
  return newNote;
}

// DELETE /notes/{id}
export async function deleteNote(id: number) {
  await api.delete(`/notes/${id}`);
}
