import styled, { keyframes } from 'styled-components';

/**
 * Animation for the spinning effect
 */
const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

/**
 * Spinner is a styled component that creates a rotating loading indicator
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
 * LoadingSpinner component that renders a spinning loading indicator
 * 
 * @returns {JSX.Element} The loading spinner
 */
export default function LoadingSpinner() {
  return <Spinner />;
}