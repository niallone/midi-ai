import Head from 'next/head';
import styled from 'styled-components';
import { MelodyGenerator } from '../components/melody/MelodyGenerator';
import { MelodyList } from '../components/melody/MelodyList';

/**
 * MainContent is a styled component that centres the main content
 * and sets a maximum width for better readability.
 */
const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

/**
 * Home is the main page component of our application.
 * It renders the header, main content (including the MelodyGenerator and MelodyList), and footer.
 * 
 * This component is responsible for:
 * 1. Setting the page title and meta description
 * 2. Rendering the overall page structure
 * 3. Including the MelodyGenerator for creating new melodies
 * 4. Displaying the MelodyList of generated melodies
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

      <MainContent>
        <h1>AI Melody Generator</h1>
        <MelodyGenerator />
        <MelodyList />
      </MainContent>
    </>
  );
}