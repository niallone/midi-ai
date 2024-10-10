import styled from 'styled-components';
import Link from 'next/link';

const HeaderWrapper = styled.header`
  background-color: ${({ theme }) => theme.colors.primary};
  color: ${({ theme }) => theme.colors.white};
  padding: 1rem 0;
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.h1`
  font-size: 1.5rem;
  margin: 0;
`;

const Nav = styled.nav`
  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
  }

  li {
    margin-left: 1rem;
  }

  a {
    color: ${({ theme }) => theme.colors.white};
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
`;

export function Header() {
  return (
    <HeaderWrapper>
      <HeaderContent>
        <Logo>AI Melody Generator</Logo>
        <Nav>
          <ul>
            <li>
              <Link href="/">Home</Link>
            </li>
            <li>
              <Link href="/about">About</Link>
            </li>
          </ul>
        </Nav>
      </HeaderContent>
    </HeaderWrapper>
  );
}