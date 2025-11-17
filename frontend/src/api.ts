import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
});

export type Note = {
  id: number;
  title: string,
  content: string
  created_at?: string;
};

// adjust paths/fields if your API is slightly different
export async function fetchNotes(): Promise<Note[]> {
  const res = await api.get("/notes");
  return res.data.map((n: any) => ({
    ...n,
    content: n.content ?? n.body ?? "",
  }));
}

export async function createNote(data: { title: string; content: string }) {
  const res = await api.post("/notes", {
    title: data.title,
    body: data.content, // IMPORTANT: backend expects "body", not "content"
  });
  return res.data as Note;
}



export async function deleteNote(id: number) {
  await api.delete(`/notes/${id}`);
}
