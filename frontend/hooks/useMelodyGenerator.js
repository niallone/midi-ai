import { useState } from 'react';
import { useMelodyContext } from '../context/MelodyContext';
import { generateMelody } from '../utils/api';

export function useMelodyGenerator() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);
  const { addMelody } = useMelodyContext();

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