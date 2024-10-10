import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useMelodyGenerator } from '../../hooks/useMelodyGenerator';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';
import ModelSelector from '../common/ModelSelector';
import { fetchModels } from '../../utils/api';

/**
 * Styled component for the generator wrapper.
 */
const GeneratorWrapper = styled.div`
  margin-bottom: 2rem;
`;

/**
 * Styled component for error messages.
 */
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.error};
`;

/**
 * MelodyGenerator component that allows users to generate new melodies.
 * It fetches available models, allows model selection, and triggers melody generation.
 *
 * @component
 * @example
 * <MelodyGenerator />
 */
export function MelodyGenerator() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const { generate, isGenerating, error } = useMelodyGenerator();

  useEffect(() => {
    // Fetch available models when the component mounts
    fetchModels()
      .then(setModels)
      .catch(error => console.error('Error fetching models:', error));
  }, []);

  const handleGenerate = () => {
    if (selectedModel) {
      generate(selectedModel);
    }
  };

  return (
    <GeneratorWrapper>
      <ModelSelector
        models={models}
        selectedModel={selectedModel}
        onSelectModel={setSelectedModel}
      />
      <Button onClick={handleGenerate} disabled={isGenerating || !selectedModel}>
        {isGenerating ? <LoadingSpinner /> : 'Generate New Melody'}
      </Button>
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </GeneratorWrapper>
  );
}