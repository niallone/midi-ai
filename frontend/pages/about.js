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
          The AI Melody Generator is an application that uses artificial intelligence models that it trains to create unique and inspiring melodies. 
          The goal is to provide musicians, composers, and music enthusiasts with a tool that can spark creativity and provide new musical ideas.
        </p>
        <p>
          Using machine learning models, the application can generate melodies in various styles and genres. 
          Whether you&apos;re looking for inspiration for your next composition or just curious about AI-generated music, this tool is here to help.
        </p>
        <p>
          I&apos;m constantly improving the models and adding new features to enhance the music creation experience. Stay tuned for updates and new capabilities.
        </p>
        <h3>About the Models</h3>
        <p>Note: The models are currently being optimised and improved with various traning and generation parameters.</p>
        <strong>V1</strong>
        <p>Version 1 was a testing model trained on 2 songs. It&apos;s not in the selection due to the pickle file not being generated, and I haven&apos;t yet looked into how to integrate and run it without the pkl file.</p>
        <strong>V2</strong>
        <p>Version 2 was trained on 25 R&B/90s Hip Hop songs and is the model that generates the most variety of notes.</p>
        <strong>V3</strong>
        <p>Version 3 was trained on about 200 Dance songs. It produces little variety of notes.</p>
        <strong>V4</strong>
        <p>Version 4 was trained on about 180 jazz songs.</p>
        <strong>V5</strong>
        <p>Version 5 is currently the better quality one and was trained on about 275 songs from various genres and years. The size of the vectors was been increased from 256 to 512 for the traning of this wodel. Also a temperature parameter has been added, which currently needs a bit more testing an optimisation.</p>
        <br/><br/>
        <p>
          <strong>Note:</strong> The some of the current models have deteriorated in quality of output. I am currently working on improving the models and the training process.
        </p>
      </MainContent>

    </>
  );
}