// components/MelodyList.js
import React from 'react';
import MelodyPlayer from './MelodyPlayer';

export default function MelodyList({ melodies }) {
  return (
    <div className="melody-list">
      <h2>Generated Melodies</h2>
      {melodies.length === 0 ? (
        <p>No melodies generated yet. Click the button to create one!</p>
      ) : (
        <ul>
          {melodies.map((melody) => (
            <li key={melody.id}>
              <h3>{melody.name}</h3>
              <MelodyPlayer url={melody.url} />
              <a href={melody.url} download>
                Download
              </a>
            </li>
          ))}
        </ul>
      )}
      <style jsx>{`
        .melody-list {
          margin-top: 20px;
        }
        ul {
          list-style-type: none;
          padding: 0;
        }
        li {
          margin-bottom: 40px;
        }
        h3 {
          margin-bottom: 10px;
        }
        a {
          color: #0070f3;
          text-decoration: none;
          margin-top: 10px;
          display: inline-block;
        }
        a:hover {
          text-decoration: underline;
        }
      `}</style>
    </div>
  );
}
