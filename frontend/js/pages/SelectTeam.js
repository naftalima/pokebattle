/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { selectTeamAction } from '../redux/actions';

function SelectTeam(props) {
  return (
    <div className="container">
      <div className="battleList">
        <Formik
          initialValues={{
            pokemon_1: '',
            pokemon_2: '',
            pokemon_3: '',
            position_1: 1,
            position_2: 2,
            position_3: 3,
          }}
          onSubmit={async (values) => {
            props.history.push('/v2/battle');
            props.selectTeamProp(values);
          }}
        >
          <Form>
            <Field id="pokemon_1" name="pokemon_1" placeholder="pikachu" type="text" />
            <Field id="pokemon_2" name="pokemon_2" placeholder="eevee" type="text" />
            <Field id="pokemon_3" name="pokemon_3" placeholder="nidorina" type="text" />
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
SelectTeam.propTypes = {
  selectTeamProp: PropTypes.func,
  history: PropTypes.object,
};
const mapStateToProps = (state) => ({
  battle: state.battleR.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    selectTeamProp: (battleForm) => {
      console.log('selectTeamProp', battleForm);
      dispatch(selectTeamAction(battleForm));
    },
  };
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SelectTeam));
