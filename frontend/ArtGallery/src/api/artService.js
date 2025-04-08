import axios from 'axios';

const BASE_URL = "http://127.0.0.1:5000";

export const getAllArt = async () => {
  const response = await axios.get(`${BASE_URL}/store/`);
  return response.data;
};

export const getArtById = async (id) => {
  const response = await axios.get(`${BASE_URL}/store/${id}`);
  return response.data;
};

// This is duplicate code from authService.js
// export const registerUser = (username, password) => {
//   return axios.post(`${BASE_URL}/auth/register`, { username, password });
// };

// This is duplicate code from authService.js
// export const loginUser = (username, password) => {
//   return axios.post(`${BASE_URL}/auth/login`, { username, password });
// };

// This is duplicate code from authService.js
// export const getProfile = (token) => {
//   return axios.get(`${BASE_URL}/auth/profile`, {
//     headers: {
//       Authorization: `Bearer ${token}`,
//     },
//   });
// };
