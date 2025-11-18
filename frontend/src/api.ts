import axios from "axios";

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
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

// PUT /notes/{id}
export async function updateNote(
  id: number,
  data: { title: string; content: string }
) {
  const res = await api.put(`/notes/${id}`, {
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

// DELETE /notes/{id}
export async function deleteNote(id: number) {
  await api.delete(`/notes/${id}`);
}

// REGISTER
export async function registerUser(data: { username: string; password: string }) {
  const res = await api.post("/auth/register", data);
  return res.data;
}

// LOGIN → returns token
export async function loginUser(data: { username: string; password: string }) {
  const res = await api.post("/auth/login", data);
  return res.data; // should include: { access_token, token_type }
}
