import React from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import BattleDetail from './pages/BattleDetail';
import BattleList from './pages/BattleList';
import store from './redux/store';
import SentryBoundary from './utils/SentryBoundary';
// import './pages/Style.scss';

const App = () => (
  <SentryBoundary>
    <Provider store={store}>
      <Router>
        <Switch>
          <Route component={BattleList} exact path="/v2/battle/" />
          <Route component={BattleDetail} exact path="/v2/battle/:id" />
        </Switch>
      </Router>
    </Provider>
  </SentryBoundary>
);

export default hot(App);
