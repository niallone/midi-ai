import React, { useEffect } from 'react';
import styled from 'styled-components';
import { useMelodyPlayer } from '../../hooks/useMelodyPlayer';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';
import MelodyVisualiser from './MelodyVisualiser';

const PlayerWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
`;

const ControlsWrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
`;

const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.error};
`;

export function MelodyPlayer({ url, isActive, onPlay }) {
  const { togglePlayback, stopPlayback, isPlaying, isLoading, error } = useMelodyPlayer(url);

  useEffect(() => {
    if (!isActive && isPlaying) {
      stopPlayback();
    }
  }, [isActive, isPlaying, stopPlayback]);

  const handlePlayPause = () => {
    if (!isPlaying) {
      onPlay();
    }
    togglePlayback();
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage>{error}</ErrorMessage>;
  }

  return (
    <PlayerWrapper>
      <ControlsWrapper>
        <Button onClick={handlePlayPause}>
          {isPlaying ? 'Pause' : 'Play'}
        </Button>
      </ControlsWrapper>
      <MelodyVisualiser midiUrl={url} />
    </PlayerWrapper>
  );
}