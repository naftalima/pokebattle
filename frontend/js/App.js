import React from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider } from 'react-redux';

import BattleDetail from './pages/BattleDetail';
import store from './redux/store';
import SentryBoundary from './utils/SentryBoundary';

const App = () => (
  <SentryBoundary>
    <Provider store={store}>
      <BattleDetail />
    </Provider>
  </SentryBoundary>
);

export default hot(App);
