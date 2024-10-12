import styled from 'styled-components';
import { Header } from './layout/Header';
import { Footer } from './layout/Footer';

const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const ContentWrapper = styled.div`
  flex: 1 0 auto;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

export function Layout({ children }) {
  return (
    <PageWrapper>
      <Header />
      <ContentWrapper>
        <MainContent>{children}</MainContent>
      </ContentWrapper>
      <Footer />
    </PageWrapper>
  );
}