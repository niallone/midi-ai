import styled from 'styled-components';

/**
 * FooterWrapper is a styled component for the footer container
 */
const FooterWrapper = styled.footer`
  background-color: ${({ theme }) => theme.colors.lightGray};
  color: ${({ theme }) => theme.colors.darkGray};
  padding: 1rem 0;
  margin-top: 2rem;
`;

/**
 * FooterContent is a styled component for the content within the footer
 */
const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
`;

/**
 * Footer component that renders the application footer
 * 
 * @returns {JSX.Element} The footer component
 */
export function Footer() {
  return (
    <FooterWrapper>
      <FooterContent>
        <p>&copy; {new Date().getFullYear()} AI Melody Generator. All rights reserved.</p>
      </FooterContent>
    </FooterWrapper>
  );
}
