import os
from music21 import converter, note, chord
import numpy as np
from tensorflow.keras.utils import to_categorical

class MIDIProcessor:
    """
    A class for processing MIDI files and preparing data for the neural network.

    This class provides methods to extract notes from MIDI files and prepare
    sequences for input to the neural network model.
    """

    def prepare_data(self, midi_directory):
        """
        Process MIDI files and extract notes and chords.

        This method walks through the specified directory, reads each MIDI file,
        and extracts the notes and chords from them.

        Args:
            midi_directory (str): Path to the directory containing MIDI files.

        Returns:
            list: Extracted notes and chords from all MIDI files.

        Raises:
            ValueError: If no MIDI files are found or no notes can be extracted.
        """
        print(f"Preparing data from directory: {midi_directory}")
        midi_files = [f for f in os.listdir(midi_directory) if f.endswith(".mid")]
        print(f"Found {len(midi_files)} MIDI files.")

        if not midi_files:
            raise ValueError("No MIDI files found. Please add some MIDI files to the midi_files directory.")

        notes = []
        for file in midi_files:
            midi_path = os.path.join(midi_directory, file)
            print(f"Processing file: {midi_path}")
            try:
                midi = converter.parse(midi_path)
                notes_to_parse = midi.flat.notes
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

        print(f"Total notes extracted: {len(notes)}")

        if not notes:
            raise ValueError("No notes were extracted from the MIDI files. Please check if the MIDI files are valid.")

        return notes

    def prepare_sequences(self, notes, sequence_length=100):
        """
        Prepare input sequences for the neural network.

        This method creates input sequences of a specified length from the
        extracted notes, and prepares corresponding output sequences.

        Args:
            notes (list): List of musical notes and chords.
            sequence_length (int): Length of each input sequence.

        Returns:
            tuple: Processed network input, output, pitch names, and note-to-integer mapping.

        Raises:
            ValueError: If the notes list is empty or no sequences could be prepared.
        """
        print(f"Preparing sequences with {len(notes)} notes...")
        if not notes:
            raise ValueError("The notes list is empty. No data to process.")
        
        # Create a set of unique pitch names
        pitchnames = sorted(set(item for item in notes))
        note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
        
        network_input = []
        network_output = []
        # Create input sequences and corresponding outputs
        for i in range(0, len(notes) - sequence_length, 1):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            network_input.append([note_to_int[char] for char in sequence_in])
            network_output.append(note_to_int[sequence_out])
        
        if not network_input or not network_output:
            raise ValueError("No sequences could be prepared. Check if the input data is sufficient.")
        
        # Reshape and normalise input
        n_patterns = len(network_input)
        network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
        network_input = network_input / float(len(pitchnames))
        network_output = to_categorical(network_output)
        
        print(f"Sequences prepared. Input shape: {network_input.shape}, Output shape: {network_output.shape}")
        return network_input, network_output, pitchnames, note_to_int