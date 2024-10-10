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
`;

/**
 * Footer component that renders the application footer.
 * It displays a copyright notice with the current year.
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
      </FooterContent>
    </FooterWrapper>
  );
}