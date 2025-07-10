// Minimal API utility for backend requests
const API_BASE = '';

let token = null;

export function setToken(newToken) {
  token = newToken;
  if (newToken) {
    localStorage.setItem('token', newToken);
  } else {
    localStorage.removeItem('token');
  }
}

export function getToken() {
  return token || localStorage.getItem('token');
}

function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export async function apiFetch(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...options.headers,
  };
  const res = await fetch(API_BASE + path, { ...options, headers });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// Auth
export const register = (data) => apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(data) });
export const login = (data) => apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(data) });
export const getProfile = () => apiFetch('/auth/profile');
export const logout = () => apiFetch('/auth/logout', { method: 'POST' });

// Store
export const getArtworks = () => apiFetch('/store/artworks');
export const getArtwork = (id) => apiFetch(`/store/artworks/${id}`);
export const getArtworkComments = (id) => apiFetch(`/store/artworks/${id}/comments`);
export const addArtworkComment = (id, content) => apiFetch(`/store/artworks/${id}/comments`, { method: 'POST', body: JSON.stringify({ content }) });
export const getUpvotes = (type, id) => apiFetch(`/store/upvote/${type}/${id}`);
export const upvote = (type, id) => apiFetch(`/store/upvote/${type}/${id}`, { method: 'POST' });
export const removeUpvote = (type, id) => apiFetch(`/store/upvote/${type}/${id}`, { method: 'DELETE' });

// Artist
export const getArtistDashboard = () => apiFetch('/artist/dashboard');
export const createArtwork = (data) => apiFetch('/artist/artwork', { method: 'POST', body: JSON.stringify(data) });
export const updateArtwork = (id, data) => apiFetch(`/artist/artwork/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteArtwork = (id) => apiFetch(`/artist/artwork/${id}`, { method: 'DELETE' });
export const getTags = () => apiFetch('/artist/tags');
export const getCategories = () => apiFetch('/artist/categories');
export const getCurrencies = () => apiFetch('/artist/currencies'); 