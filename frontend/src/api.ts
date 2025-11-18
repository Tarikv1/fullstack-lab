import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
});

// Attach Authorization header if a token exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---------- AUTH ----------

// REGISTER: POST /users/signup with JSON body { email, password }
export async function registerUser(data: { email: string; password: string }) {
  const res = await api.post("/users/signup", {
    email: data.email,
    password: data.password,
  });
  return res.data; // user object
}

// LOGIN: POST /auth/token with x-www-form-urlencoded (username=email)
export async function loginUser(data: { email: string; password: string }) {
  const formData = new URLSearchParams();
  formData.append("username", data.email);
  formData.append("password", data.password);

  const res = await api.post("/auth/token", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  // expected: { access_token, token_type: "bearer" }
  return res.data;
}

// ---------- NOTES ----------

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
