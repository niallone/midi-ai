// components/MelodyPlayer.js
import React, { useEffect, useState, useRef } from 'react';
import * as Tone from 'tone';
import { Midi } from '@tonejs/midi';
import styles from './MelodyPlayer.module.css';

const MelodyPlayer = ({ url }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [midi, setMidi] = useState(null);
  const canvasRef = useRef(null);
  const synthRef = useRef(null);

  useEffect(() => {
    // Fetch the MIDI file and parse it
    fetch(url)
      .then((response) => response.arrayBuffer())
      .then((arrayBuffer) => {
        const midiData = new Midi(arrayBuffer);
        setMidi(midiData);
        drawVisualization(midiData);
      })
      .catch((err) => {
        console.error('Error loading MIDI file:', err);
      });

    // Cleanup function to dispose of the synth
    return () => {
      if (synthRef.current) {
        synthRef.current.dispose();
      }
    };
  }, [url]);

  const drawVisualization = (midiData) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    const notes = midiData.tracks.flatMap((track) => track.notes);

    const maxTime = notes.reduce(
      (max, note) => Math.max(max, note.time + note.duration),
      0
    );

    notes.forEach((note) => {
      const x = (note.time / maxTime) * width;
      const w = (note.duration / maxTime) * width;
      const y = ((108 - note.midi) / (108 - 21)) * height;
      const noteHeight = height / (108 - 21);

      ctx.fillStyle = 'blue';
      ctx.fillRect(x, y, w, noteHeight);
    });
  };

  const startPlayback = async () => {
    if (!midi) return;

    await Tone.start();

    const now = Tone.now() + 0.5; // Add a slight delay to avoid clicks

    synthRef.current = new Tone.PolySynth(Tone.Synth).toDestination();

    midi.tracks.forEach((track) => {
      track.notes.forEach((note) => {
        synthRef.current.triggerAttackRelease(
          note.name,
          note.duration,
          note.time + now,
          note.velocity
        );
      });
    });

    setIsPlaying(true);
  };

  const stopPlayback = () => {
    if (synthRef.current) {
      synthRef.current.releaseAll();
      synthRef.current.dispose();
      synthRef.current = null;
    }
    setIsPlaying(false);
  };

  return (
    <div className={styles.melodyPlayer}>
      <button onClick={isPlaying ? stopPlayback : startPlayback}>
        {isPlaying ? 'Stop' : 'Play'}
      </button>
      <canvas ref={canvasRef} width={600} height={200} />
    </div>
  );
};

export default MelodyPlayer;
