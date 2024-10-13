/**
 * Theme configuration for styled-components
 * This object defines the global styles and variables used throughout the application.
 */
const theme = {
  /**
   * Colour palette for the application
   */
  colors: {
    primary: '#82DEAF',
    primaryDark: '#4E8A6B',
    secondary: '#ff4081',
    white: '#ffffff',
    black: '#000000',
    lightGray: '#f0f0f0',
    darkGray: '#333333',
    error: '#ff3d00',
    success: '#00c853',
    disabled: '#cccccc',
  },
  /**
   * Font families used in the application
   */
  fonts: {
    body: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif',
    heading: 'Georgia, serif',
  },
  /**
   * Font sizes for different text elements
   */
  fontSizes: {
    small: '0.875rem',
    medium: '1rem',
    large: '1.25rem',
    xlarge: '1.5rem',
  },
  /**
   * Spacing values for margins, paddings, etc.
   */
  spacing: {
    small: '0.5rem',
    medium: '1rem',
    large: '1.5rem',
    xlarge: '2rem',
  },
  /**
   * Breakpoints for responsive design
   */
  breakpoints: {
    mobile: '480px',
    tablet: '768px',
    desktop: '1024px',
  },
};

export default theme;