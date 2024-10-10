import React from 'react';
import styled from 'styled-components';

const SelectWrapper = styled.div`
  margin-bottom: 1rem;
`;

const StyledSelect = styled.select`
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid ${({ theme }) => theme.colors.primary};
  border-radius: 4px;
`;

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