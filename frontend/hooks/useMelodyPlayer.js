import { useState, useEffect, useRef, useCallback } from 'react';
import { start, PolySynth, Synth, now, Transport } from 'tone';
import { Midi } from '@tonejs/midi';

/**
 * Custom hook for managing melody playback.
 * 
 * @param {string} url - The URL of the MIDI file to play
 * @returns {Object} An object containing playback control functions and state
 * @property {function} togglePlayback - Function to toggle play/pause
 * @property {function} stopPlayback - Function to stop playback
 * @property {boolean} isPlaying - Whether the melody is currently playing
 * @property {boolean} isLoading - Whether the melody is currently loading
 * @property {string|null} error - Error message if loading or playback fails
 */
export function useMelodyPlayer(url) {
  // State for tracking playback status
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Refs to persist values across re-renders without causing effects
  const synthRef = useRef(null);  // Stores the Tone.js synthesiser
  const midiRef = useRef(null);   // Stores the parsed MIDI data
  const eventsRef = useRef([]);   // Stores scheduled playback events

  // Function to clean up playback resources
  const cleanupPlayback = useCallback(() => {
    // Dispose of the synthesiser if it exists
    if (synthRef.current) {
      synthRef.current.disconnect();
      synthRef.current.dispose();
      synthRef.current = null;
    }
    // Stop and clear all scheduled events from Tone.js Transport
    Transport.stop();
    Transport.cancel();
    eventsRef.current.forEach((event) => Transport.clear(event));
    eventsRef.current = [];
  }, []);

  // Effect to load MIDI file when URL changes
  useEffect(() => {
    const loadMidi = async () => {
      cleanupPlayback();
      setIsLoading(true);
      setError(null);
      try {
        // Fetch and parse the MIDI file
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

    // Cleanup function for when component unmounts or URL changes
    return cleanupPlayback;
  }, [url, cleanupPlayback]);

  // Function to schedule MIDI events for playback
  const scheduleMelody = useCallback(() => {
    const nowTime = now();
    midiRef.current.tracks.forEach((track) => {
      track.notes.forEach((note) => {
        // Schedule each note to be played at the correct time
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

  // Function to toggle playback
  const togglePlayback = useCallback(async () => {
    if (!midiRef.current) return;

    // Ensure audio context is started (necessary for browsers with autoplay policies)
    await start();

    if (isPlaying) {
      // If playing, pause the transport
      Transport.pause();
    } else {
      // If not playing, create synth if it doesn't exist and start playback
      if (!synthRef.current) {
        synthRef.current = new PolySynth(Synth).toDestination();
        scheduleMelody();
      }
      Transport.start();
    }

    // Toggle playing state
    setIsPlaying(!isPlaying);
  }, [isPlaying, scheduleMelody]);

  // Function to stop playback
  const stopPlayback = useCallback(() => {
    if (isPlaying) {
      cleanupPlayback();
      setIsPlaying(false);
    }
  }, [isPlaying, cleanupPlayback]);

  // Return functions and state for use in components
  return { togglePlayback, stopPlayback, isPlaying, isLoading, error };
}