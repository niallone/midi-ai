import React, { useEffect, useRef } from 'react';
import { Midi } from '@tonejs/midi';

/**
 * MelodyVisualiser component that renders a visual representation of a MIDI file.
 * It creates a piano roll-style visualisation using HTML5 canvas.
 *
 * @component
 * @param {Object} props - The component props
 * @param {string} props.midiUrl - The URL of the MIDI file to visualise
 *
 * @example
 * <MelodyVisualiser midiUrl="https://example.com/path/to/midi/file.mid" />
 */
const MelodyVisualiser = ({ midiUrl }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const loadAndVisualiseMidi = async () => {
      // Fetch and parse the MIDI file
      const response = await fetch(midiUrl);
      const arrayBuffer = await response.arrayBuffer();
      const midi = new Midi(arrayBuffer);

      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      // Set canvas size
      canvas.width = 600;
      canvas.height = 200;

      // Clear canvas
      ctx.fillStyle = '#333333';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw piano roll
      const noteHeight = 2;
      const pixelsPerTick = canvas.width / midi.durationTicks;

      midi.tracks.forEach((track) => {
        track.notes.forEach((note) => {
          const x = note.ticks * pixelsPerTick;
          const y = canvas.height - (note.midi - 21) * noteHeight;
          const width = note.durationTicks * pixelsPerTick;
          
          // Use HSL colour to represent different pitches
          ctx.fillStyle = `hsl(${note.midi * 2}, 100%, 50%)`;
          ctx.fillRect(x, y, width, noteHeight);
        });
      });
    };

    loadAndVisualiseMidi();
  }, [midiUrl]);

  return (
    <div className="melody-visualiser">
      <canvas ref={canvasRef} style={{ width: '100%', height: 'auto' }} />
    </div>
  );
};

export default MelodyVisualiser;