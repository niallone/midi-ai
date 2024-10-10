import { ThemeProvider } from 'styled-components';
import { MelodyProvider } from '../context/MelodyContext';
import theme from '../styles/theme';
import '../styles/globals.css';

/**
 * MelodyGenerator is the top-level component in our Next.js application.
 * It wraps all other components and provides global functionality.
 * 
 * This component is responsible for:
 * 1. Applying the global CSS styles
 * 2. Providing the theme via ThemeProvider from styled-components
 * 3. Providing the MelodyContext via MelodyProvider
 * 
 * @param {Object} props - The component props
 * @param {React.Component} props.Component - The active page component
 * @param {Object} props.pageProps - The initial props preloaded for the page
 * @returns {React.Component} The wrapped application component
 */
function MelodyGenerator({ Component, pageProps }) {
  return (
    // ThemeProvider allows us to use a consistent theme across our styled-components
    <ThemeProvider theme={theme}>
      {/* MelodyProvider gives all child components access to our melody context */}
      <MelodyProvider>
        {/* Render the active page component */}
        <Component {...pageProps} />
      </MelodyProvider>
    </ThemeProvider>
  );
}

export default MelodyGenerator;