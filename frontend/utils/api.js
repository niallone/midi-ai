import axios from 'axios';

/**
 * The base URL for API requests.
 * It uses the environment variable if set, otherwise defaults to localhost.
 */
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4050';

/**
 * Fetches the list of available melody generation models from the API.
 * 
 * @returns {Promise<Array>} A promise that resolves to an array of model objects
 * @throws Will throw an error if the API request fails
 */
export async function fetchModels() {
  try {
    const response = await axios.get(`${API_URL}/melody/models`);
    return response.data;
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
}

/**
 * Generates a new melody using the specified model.
 * 
 * @param {string} modelId - The ID of the model to use for generation
 * @returns {Promise<Object>} A promise that resolves to an object containing the generated melody info
 * @throws Will throw an error if the API request fails
 */
export async function generateMelody(modelId) {
  try {
    const response = await axios.post(`${API_URL}/melody/generate`, { model_id: modelId });
    return {
      id: Date.now(),
      name: response.data.file_name,
      url: `${API_URL}/melody/download/${response.data.file_name}`,
    };
  } catch (error) {
    console.error('Error generating melody:', error);
    throw error;
  }
}