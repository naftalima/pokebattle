/* eslint-disable jsx-a11y/label-has-associated-control */
import React from 'react';

import FormOpponent from '../components/FormOpponent';

export default function CreateBattle() {
  return (
    <div className="container">
      <div className="battleList">
        <h1 className="title">Choose your Opponent!</h1>
        <FormOpponent />
      </div>
    </div>
  );
}
