import React, { useState } from 'react';

const SpeedInsights = () => {
  const [url, setUrl] = useState('');
  const [insights, setInsights] = useState(null);

  const fetchInsights = async () => {
    const response = await fetch(`/api/speed-insights?url=${encodeURIComponent(url)}`);
    const data = await response.json();
    setInsights(data);
  };

  return (
    <div>
      <h1>Speed Insights</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL"
      />
      <button onClick={fetchInsights}>Get Insights</button>
      {insights && (
        <pre>{JSON.stringify(insights, null, 2)}</pre>
      )}
    </div>
  );
};

export default SpeedInsights;
