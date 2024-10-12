import Head from 'next/head';
import styled from 'styled-components';

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

export default function About() {
  return (
    <>
      <Head>
        <title>About - AI Melody Generator</title>
        <meta name="description" content="Learn about the AI Melody Generator" />
      </Head>

      <MainContent>
        <h1>About AI Melody Generator</h1>
        <p>
          The AI Melody Generator is an application that uses artificial intelligence models that it trains
          to create unique and inspiring melodies. The goal is to provide musicians, composers,
          and music enthusiasts with a tool that can spark creativity and provide new musical ideas.
        </p>
        <p>
          Using state-of-the-art machine learning models, the application can generate melodies
          in various styles and genres. Whether you&apos;re looking for inspiration for your next
          composition or just curious about AI-generated music, this tool is here to help.
        </p>
        <p>
          We&apos;re constantly improving the models and adding new features to enhance your
          music creation experience. Stay tuned for updates and new capabilities!
        </p>
      </MainContent>

    </>
  );
}