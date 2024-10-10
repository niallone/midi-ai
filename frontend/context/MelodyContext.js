import { createContext, useContext, useState } from 'react';

/**
 * MelodyContext is used to share melody-related state across components
 * without having to pass props manually at every level.
 */
const MelodyContext = createContext();

/**
 * MelodyProvider component that wraps the app and provides melody context.
 * 
 * @param {Object} props - The component props
 * @param {React.ReactNode} props.children - The child components
 * @returns {JSX.Element} The provider component
 */
export function MelodyProvider({ children }) {
  // State to store all generated melodies
  const [melodies, setMelodies] = useState([]);

  /**
   * Function to add a new melody to the state
   * 
   * @param {Object} melody - The melody object to add
   */
  const addMelody = (melody) => {
    setMelodies((prevMelodies) => [...prevMelodies, melody]);
  };

  // The value object that will be shared with all children components
  const value = { melodies, addMelody };

  return (
    <MelodyContext.Provider value={value}>
      {children}
    </MelodyContext.Provider>
  );
}

/**
 * Custom hook to use the melody context
 * 
 * @returns {Object} The melody context value
 */
export function useMelodyContext() {
  return useContext(MelodyContext);
}