import { useState, useEffect, useRef, useCallback } from 'react';
import { start, PolySynth, Synth, now, Transport } from 'tone';
import { Midi } from '@tonejs/midi';

export function useMelodyPlayer(url) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const synthRef = useRef(null);
  const midiRef = useRef(null);
  const eventsRef = useRef([]);

  const cleanupPlayback = useCallback(() => {
    if (synthRef.current) {
      synthRef.current.disconnect();
      synthRef.current.dispose();
      synthRef.current = null;
    }
    Transport.stop();
    Transport.cancel();
    eventsRef.current.forEach((event) => Transport.clear(event));
    eventsRef.current = [];
  }, []);

  useEffect(() => {
    const loadMidi = async () => {
      cleanupPlayback();
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(url);
        const arrayBuffer = await response.arrayBuffer();
        midiRef.current = new Midi(arrayBuffer);
        setIsLoading(false);
      } catch (err) {
        console.error('Error loading MIDI file:', err);
        setError('Failed to load melody. Please try again.');
        setIsLoading(false);
      }
    };

    loadMidi();

    return cleanupPlayback;
  }, [url, cleanupPlayback]);

  const scheduleMelody = useCallback(() => {
    const nowTime = now();
    midiRef.current.tracks.forEach((track) => {
      track.notes.forEach((note) => {
        const event = Transport.schedule((time) => {
          synthRef.current.triggerAttackRelease(
            note.name,
            note.duration,
            time,
            note.velocity
          );
        }, note.time + nowTime);
        eventsRef.current.push(event);
      });
    });
  }, []);

  const togglePlayback = useCallback(async () => {
    if (!midiRef.current) return;

    await start();

    if (isPlaying) {
      Transport.pause();
    } else {
      if (!synthRef.current) {
        synthRef.current = new PolySynth(Synth).toDestination();
        scheduleMelody();
      }
      Transport.start();
    }

    setIsPlaying(!isPlaying);
  }, [isPlaying, scheduleMelody]);

  const stopPlayback = useCallback(() => {
    if (isPlaying) {
      cleanupPlayback();
      setIsPlaying(false);
    }
  }, [isPlaying, cleanupPlayback]);

  return { togglePlayback, stopPlayback, isPlaying, isLoading, error };
}