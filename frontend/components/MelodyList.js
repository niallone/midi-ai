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
                <a href={melody.url} download>
                  {melody.name}
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
            margin-bottom: 10px;
          }
          a {
            color: #0070f3;
            text-decoration: none;
          }
          a:hover {
            text-decoration: underline;
          }
        `}</style>
      </div>
    );
  }