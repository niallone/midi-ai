import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useMelodyGenerator } from '../../hooks/useMelodyGenerator';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';
import ModelSelector from './ModelSelector';
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

const LoadingWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px; // Adjust this value to match the height of your ModelSelector
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
  const {generate, isGenerating, error} = useMelodyGenerator();
  const [isLoadingModels, setIsLoadingModels] = useState(true);
  const [modelError, setModelError] = useState(null);

  useEffect(() => {
    const loadModels = async () => {
      try {
        setIsLoadingModels(true);
        const fetchedModels = await fetchModels();
        setModels(fetchedModels);
        setModelError(null);
      } catch (error) {
        console.error('Error fetching models:', error);
        setModelError('Failed to load models. Please try again later.');
      } finally {
        setIsLoadingModels(false);
      }
    };

    loadModels();
  }, []);

  const handleGenerate = () => {
    if (selectedModel) {
      generate(selectedModel);
    }
  };

  return (
    <GeneratorWrapper>
      {isLoadingModels ? (
        <LoadingWrapper>
          <LoadingSpinner />
        </LoadingWrapper>
      ) : modelError ? (
        <ErrorMessage>{modelError}</ErrorMessage>
      ) : (
        <ModelSelector
          models={models}
          selectedModel={selectedModel}
          onSelectModel={setSelectedModel}
        />
      )}
      <Button onClick={handleGenerate} disabled={isGenerating || !selectedModel || isLoadingModels}>
        {isGenerating ? <LoadingSpinner /> : 'Generate New Melody'}
      </Button>
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </GeneratorWrapper>
  );
}