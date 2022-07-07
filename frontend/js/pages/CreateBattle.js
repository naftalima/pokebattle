import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { withRouter } from 'react-router';

import { createBattleApi } from '../utils/api';

function CreateBattle(props) {
  return (
    <div className="container">
      <div className="battleList">
        <Formik
          initialValues={{
            opponent: '',
          }}
          onSubmit={async (values) => {
            createBattleApi(values).then((battle) => {
              const { teams } = battle;
              const creatorTeamId = teams[0].id;
              props.history.push(`/v2/team/${creatorTeamId}`);
              return true;
            });
          }}
        >
          <Form>
            <Field id="opponent" name="opponent" placeholder="jane@acme.com" type="email" />
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
CreateBattle.propTypes = {
  history: PropTypes.object,
};

export default withRouter(CreateBattle);
