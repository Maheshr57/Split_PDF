export default function handler(req, res) {
  const speedData = {
    // Sample speed insights data
    firstContentfulPaint: '1.2s',
    largestContentfulPaint: '2.5s',
    totalBlockingTime: '150ms',
    cumulativeLayoutShift: '0.1',
  };

  res.status(200).json(speedData);
}
