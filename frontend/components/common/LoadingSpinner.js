import styled, { keyframes } from 'styled-components';

/**
 * Animation for the spinning effect.
 * Creates a 360-degree rotation animation.
 */
const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

/**
 * Spinner is a styled component that creates a rotating loading indicator.
 * It uses the theme colours for styling and the spin animation for rotation.
 */
const Spinner = styled.div`
  border: 4px solid ${({ theme }) => theme.colors.lightGray};
  border-top: 4px solid ${({ theme }) => theme.colors.primary};
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: ${spin} 1s linear infinite;
`;

/**
 * LoadingSpinner component that renders a spinning loading indicator.
 * Use this component to indicate that content is loading or an action is in progress.
 *
 * @component
 * @example
 * <LoadingSpinner />
 *
 * @example
 * // Inside a container with custom styles
 * <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
 *   <LoadingSpinner />
 * </div>
 */
export default function LoadingSpinner() {
  return <Spinner />;
}