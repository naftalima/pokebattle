import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { createBattleAction } from '../redux/actions';

function CreateBattle(props) {
  return (
    <div className="container">
      <div className="battleList">
        <Formik
          initialValues={{
            opponent: '',
          }}
          onSubmit={async (values) => {
            props.createBattleAction(values);
            const teamId = 39;
            props.history.push(`/v2/team/${teamId}`);
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
  createBattleAction: PropTypes.func,
  history: PropTypes.object,
};
const mapStateToProps = (state) => ({
  battle: state.battleR.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    createBattleAction: (battleForm) => dispatch(createBattleAction(battleForm)),
  };
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(CreateBattle));
