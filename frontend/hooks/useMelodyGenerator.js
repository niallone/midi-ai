import { useState } from 'react';
import { useMelodyContext } from '../context/MelodyContext';
import { generateMelody } from '../utils/api';

/**
 * Custom hook for generating melodies.
 * It manages the state of melody generation and interacts with the MelodyContext.
 * 
 * @returns {Object} An object containing the generate function and state
 * @property {function} generate - Function to generate a new melody
 * @property {boolean} isGenerating - Whether a melody is currently being generated
 * @property {string|null} error - Error message if generation fails
 */
export function useMelodyGenerator() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);
  const { addMelody } = useMelodyContext();

  /**
   * Generates a new melody using the specified model.
   * 
   * @param {string} modelId - The ID of the model to use for generation
   */
  const generate = async (modelId) => {
    setIsGenerating(true);
    setError(null);

    try {
      const newMelody = await generateMelody(modelId);
      addMelody(newMelody);
    } catch (err) {
      setError('Failed to generate melody. Please try again.');
      console.error('Error generating melody:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return { generate, isGenerating, error };
}