/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { withRouter } from 'react-router';

import { createBattleApi } from '../utils/api';

function FormOpponent(props) {
  const { history } = props;
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
FormOpponent.propTypes = {
  history: PropTypes.object,
};

export default withRouter(FormOpponent);
