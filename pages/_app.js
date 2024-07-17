import '../styles/globals.css';
import SpeedInsights from '../components/SpeedInsights';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Component {...pageProps} />
      <SpeedInsights />
    </>
  );
}

export default MyApp;
