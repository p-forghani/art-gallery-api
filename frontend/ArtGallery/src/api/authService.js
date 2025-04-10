import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const registerUser = (name, email, password) => {
  return axios.post(`${API_URL}/auth/register`, { name, email, password });
};

export const loginUser = (email, password) => {
  return axios.post(`${API_URL}/auth/login`, { email, password });
};

export const getProfile = (token) => {
  return axios.get(`${API_URL}/auth/profile`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

// This is duplicate code from artService.js
// export const getAllArt = () => {
//   return axios.get(`${API_URL}/store/`);
// };

// export const getArtById = (id) => {
//   return axios.get(`${API_URL}/store/${id}`);
// };

