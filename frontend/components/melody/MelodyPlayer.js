import React, { useEffect } from 'react';
import styled from 'styled-components';
import { useMelodyPlayer } from '../../hooks/useMelodyPlayer';
import Button from '../common/Button';
import LoadingSpinner from '../common/LoadingSpinner';
import MelodyVisualiser from './MelodyVisualiser';

/**
 * Styled component for the player wrapper.
 */
const PlayerWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
`;

/**
 * Styled component for the controls wrapper.
 */
const ControlsWrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
`;

/**
 * Styled component for error messages.
 */
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.error};
`;

/**
 * MelodyPlayer component that provides playback controls and visualisation for a melody.
 * It uses the useMelodyPlayer hook to manage playback state and control.
 *
 * @component
 * @param {Object} props - The component props
 * @param {string} props.url - The URL of the melody file
 * @param {boolean} props.isActive - Whether this player is currently active
 * @param {function} props.onPlay - Callback function to be called when play is initiated
 *
 * @example
 * <MelodyPlayer 
 *   url="https://example.com/path/to/melody.mid"
 *   isActive={true}
 *   onPlay={() => console.log('Playback started')}
 * />
 */
export function MelodyPlayer({ url, isActive, onPlay }) {
  const { togglePlayback, stopPlayback, isPlaying, isLoading, error } = useMelodyPlayer(url);

  useEffect(() => {
    // Stop playback if this player becomes inactive
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