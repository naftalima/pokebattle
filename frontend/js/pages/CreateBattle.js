/* eslint-disable jsx-a11y/label-has-associated-control */
import React from 'react';
import { withRouter } from 'react-router';

import FormOpponent from '../components/FormOpponent';

function CreateBattle() {
  return (
    <div className="container">
      <div className="battleList">
        <h1 className="title">Choose your Opponent!</h1>
        <FormOpponent />
      </div>
    </div>
  );
}

export default withRouter(CreateBattle);
