import styled from 'styled-components';

/**
 * Card is a styled component that creates a simple card layout.
 * It applies a background colour, border radius, and box shadow to create a raised effect.
 *
 * @component
 * @example
 * <Card>
 *   <h2>Card Title</h2>
 *   <p>Card content goes here.</p>
 * </Card>
 */
const Card = styled.div`
  background-color: ${({ theme }) => theme.colors.white};
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
`;

export default Card;