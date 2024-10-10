import React, { useState } from 'react';
import styled from 'styled-components';
import { useMelodyContext } from '../../context/MelodyContext';
import { MelodyPlayer } from './MelodyPlayer';
import Card from '../common/Card';

/**
 * Styled component for the melody list wrapper.
 */
const MelodyListWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

/**
 * Styled component for individual melody items.
 */
const MelodyItem = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
`;

/**
 * Styled component for melody titles.
 */
const MelodyTitle = styled.h3`
  margin-bottom: 1rem;
`;

/**
 * Styled component for download links.
 */
const DownloadLink = styled.a`
  margin-top: 1rem;
  color: ${({ theme }) => theme.colors.primary};
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

/**
 * MelodyList component that displays a list of generated melodies.
 * It uses the MelodyContext to access the list of melodies and renders
 * a MelodyPlayer for each melody. It also manages the currently active
 * melody to ensure only one plays at a time.
 *
 * @component
 * @example
 * <MelodyList />
 */
export function MelodyList() {
  const { melodies } = useMelodyContext();
  const [activeMelodyId, setActiveMelodyId] = useState(null);

  // If no melodies have been generated, display a message
  if (melodies.length === 0) {
    return <p>No melodies generated yet. Click the button to create one!</p>;
  }

  return (
    <MelodyListWrapper>
      {melodies.map((melody) => (
        <MelodyItem key={melody.id}>
          <MelodyTitle>{melody.name}</MelodyTitle>
          <MelodyPlayer 
            url={melody.url} 
            isActive={activeMelodyId === melody.id}
            onPlay={() => setActiveMelodyId(melody.id)}
          />
          <DownloadLink href={melody.url} download>
            Download
          </DownloadLink>
        </MelodyItem>
      ))}
    </MelodyListWrapper>
  );
}