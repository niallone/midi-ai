import React, { useState } from 'react';
import styled from 'styled-components';
import { useMelodyContext } from '../../context/MelodyContext';
import { MelodyPlayer } from './MelodyPlayer';
import Card from '../common/Card';

const MelodyListWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const MelodyItem = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
`;

const MelodyTitle = styled.h3`
  margin-bottom: 1rem;
`;

const DownloadLink = styled.a`
  margin-top: 1rem;
  color: ${({ theme }) => theme.colors.primary};
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

export function MelodyList() {
  const { melodies } = useMelodyContext();
  const [activeMelodyId, setActiveMelodyId] = useState(null);

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