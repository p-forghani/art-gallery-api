// API service for connecting to Flask backend

// Base URL of your Flask API
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Fetch all art cards from the Flask backend
 * @returns {Promise} Promise that resolves to array of card data
 */
export const getAllCards = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/cards`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching cards:', error);
    return {};
  }
};

/**
 * Fetch a single card by ID from the Flask backend
 * @param {string} cardId - ID of the card to fetch
 * @returns {Promise} Promise that resolves to card data
 */
export const getCardById = async (cardId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/cards/${cardId}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error fetching card ${cardId}:`, error);
    return {};
  }
}; 