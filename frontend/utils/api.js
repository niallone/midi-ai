import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4050';

export async function fetchModels() {
  try {
    const response = await axios.get(`${API_URL}/api/models`);
    return response.data;
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
}

export async function generateMelody(modelId) {
  try {
    const response = await axios.post(`${API_URL}/generate`, { model_id: modelId });
    return {
      id: Date.now(),
      name: response.data.file_name,
      url: `${API_URL}/download/${response.data.file_name}`,
    };
  } catch (error) {
    console.error('Error generating melody:', error);
    throw error;
  }
}