import React from 'react';
import styled from 'styled-components';

/**
 * FooterWrapper is a styled component for the footer container.
 * It provides background colour, text colour, and spacing for the footer.
 */
const FooterWrapper = styled.footer`
  background-color: ${({ theme }) => theme.colors.lightGray};
  color: ${({ theme }) => theme.colors.darkGray};
  padding: 1rem 0;
  margin-top: 2rem;
`;

/**
 * FooterContent is a styled component for the content within the footer.
 * It centers the content and sets a maximum width for responsiveness.
 */
const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
`;

/**
 * StyledLink is a styled component for the GitHub link.
 * It removes the default underline and sets the color.
 */
const StyledLink = styled.a`
  text-decoration: none;
  color: ${({ theme }) => theme.colors.darkGray};
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    text-decoration: underline;
  }
`;

/**
 * Footer component that renders the application footer.
 * It displays a copyright notice with the current year and a GitHub link.
 *
 * @component
 * @example
 * <Footer />
 *
 * @example
 * // In a page layout
 * <div>
 *   <Header />
 *   <main>{pageContent}</main>
 *   <Footer />
 * </div>
 */
export function Footer() {
  return (
    <FooterWrapper>
      <FooterContent>
        <p>&copy; {new Date().getFullYear()} AI Melody Generator.</p>
        <StyledLink href="https://github.com/niallone/midi-ai" target="_blank" rel="noopener noreferrer">
          GitHub
        </StyledLink>
      </FooterContent>
    </FooterWrapper>
  );
}