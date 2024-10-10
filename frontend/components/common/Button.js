import styled from 'styled-components';

/**
 * Button is a styled component that creates a customisable button.
 * It utilises theme colours and applies hover and disabled states.
 *
 * @component
 * @example
 * <Button onClick={() => console.log('Button clicked')}>Click me</Button>
 *
 * @example
 * <Button disabled>Disabled Button</Button>
 */
const Button = styled.button`
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.white};
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;

  /* Hover state */
  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryDark};
  }

  /* Disabled state */
  &:disabled {
    background-color: ${({ theme }) => theme.colors.disabled};
    cursor: not-allowed;
  }
`;

export default Button;