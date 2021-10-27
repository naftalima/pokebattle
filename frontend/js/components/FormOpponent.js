/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import React from 'react';
import { useHistory } from 'react-router-dom';

import { createBattleApi } from '../utils/api';

export default function FormOpponent() {
  const history = useHistory();

  return (
    <Formik
      initialValues={{
        opponent: '',
      }}
      onSubmit={async (values) => {
        createBattleApi(values).then((battle) => {
          const { teams } = battle;
          const creatorTeamId = teams[0].id;
          history.push(`/v2/team/${creatorTeamId}`);
          return true;
        });
      }}
    >
      <Form>
        <div>
          <label htmlFor="opponent">Opponent:</label>
          <Field id="opponent" name="opponent" placeholder="jane@doe.com" type="email" />
        </div>
        <button className="battle-id-btn" type="submit">
          Submit
        </button>
      </Form>
    </Formik>
  );
}
