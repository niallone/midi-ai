export default function GenerateButton({ onGenerate }) {
    return (
      <button onClick={onGenerate} className="generate-button">
        Generate New Melody
        <style jsx>{`
          .generate-button {
            background-color: #0070f3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
          }
          .generate-button:hover {
            background-color: #0051bb;
          }
        `}</style>
      </button>
    );
  }