import React from 'react';
import { hot } from 'react-hot-loader/root';

// import Home from './pages/Home';
import BattleDetail from './components/battles/BattleDetail';
import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
    <BattleDetail />
  </SentryBoundary>
);

export default hot(App);
