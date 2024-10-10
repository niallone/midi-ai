import { useState } from 'react';
import Head from 'next/head';
import axios from 'axios';
import styles from '../styles/Home.module.css';
import GenerateButton from '../components/GenerateButton';
import MelodyList from '../components/MelodyList';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4050';

export default function Home() {
    const [melodies, setMelodies] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
  
    const handleGenerateMelody = async () => {
      setIsLoading(true);
      setError(null);
      try {
        console.log('Sending request to:', `${API_URL}/generate`);
        const response = await axios.post(`${API_URL}/generate`);
        console.log('Response received:', response.data);
        const newMelody = {
          id: Date.now(),
          name: response.data.file_name,
          url: `${API_URL}/download/${response.data.file_name}`
        };
        setMelodies([...melodies, newMelody]);
      } catch (err) {
        console.error('Error generating melody:', err);
        setError(`Failed to generate melody. Error: ${err.message}`);
      } finally {
        setIsLoading(false);
      }
    };

  return (
    <div className={styles.container}>
      <Head>
        <title>Melody Generator</title>
        <meta name="description" content="Generate unique melodies with AI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Melody Generator</h1>
        <GenerateButton onGenerate={handleGenerateMelody} isLoading={isLoading} />
        {error && <p className={styles.error}>{error}</p>}
        <MelodyList melodies={melodies} />
      </main>

    </div>
  );
}