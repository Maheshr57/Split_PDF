import React, { useEffect, useState } from 'react';

const SpeedInsights = () => {
  const [speedData, setSpeedData] = useState(null);

  useEffect(() => {
    // Fetch speed insights data from an API or service
    fetch('/api/speed-insights')
      .then(response => response.json())
      .then(data => setSpeedData(data))
      .catch(error => console.error('Error fetching speed insights:', error));
  }, []);

  if (!speedData) {
    return <div>Loading speed insights...</div>;
  }

  return (
    <div>
      <h2>Speed Insights</h2>
      <pre>{JSON.stringify(speedData, null, 2)}</pre>
    </div>
  );
};

export default SpeedInsights;
