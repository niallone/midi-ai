import React from 'react';
import styled from 'styled-components';

/**
 * Styled wrapper for the select element to provide consistent spacing.
 */
const SelectWrapper = styled.div`
  margin-bottom: 1rem;
`;

/**
 * Styled select element with custom appearance.
 */
const StyledSelect = styled.select`
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.primary};
  border-radius: 4px;
`;

/**
 * ModelSelector component allows users to select a model from a list of options.
 *
 * @component
 * @param {Object} props - The component props
 * @param {Array} props.models - An array of model objects, each containing 'id' and 'name' properties
 * @param {string} props.selectedModel - The currently selected model ID
 * @param {function} props.onSelectModel - Callback function to handle model selection changes
 *
 * @example
 * const models = [
 *   { id: '1', name: 'Model A' },
 *   { id: '2', name: 'Model B' },
 * ];
 * const [selectedModel, setSelectedModel] = useState('');
 *
 * <ModelSelector
 *   models={models}
 *   selectedModel={selectedModel}
 *   onSelectModel={setSelectedModel}
 * />
 */
const ModelSelector = ({ models, selectedModel, onSelectModel }) => {
  return (
    <SelectWrapper>
      <StyledSelect value={selectedModel} onChange={(e) => onSelectModel(e.target.value)}>
        <option value="">Select a model</option>
        {models.map((model) => (
          <option key={model.id} value={model.id}>
            {model.name}
          </option>
        ))}
      </StyledSelect>
    </SelectWrapper>
  );
};

export default ModelSelector;