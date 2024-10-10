import Head from 'next/head';
import styled from 'styled-components';
import { Header } from '../components/layout/Header';
import { Footer } from '../components/layout/Footer';
import { MelodyGenerator } from '../components/melody/MelodyGenerator';
import { MelodyList } from '../components/melody/MelodyList';

/**
 * MainContent is a styled component that centers the main content
 * and sets a maximum width for better readability.
 */
const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

/**
 * Home is the main page component of our application.
 * It renders the header, main content, and footer.
 * 
 * @returns {JSX.Element} The home page structure
 */
export default function Home() {
  return (
    <>
      <Head>
        <title>AI Melody Generator</title>
        <meta name="description" content="Generate unique melodies with AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <MainContent>
        <h1>AI Melody Generator</h1>
        <MelodyGenerator />
        <MelodyList />
      </MainContent>

      <Footer />
    </>
  );
}