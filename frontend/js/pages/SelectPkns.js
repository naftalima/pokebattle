import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { selectTeamAction } from '../redux/actions';

function SelectPkns(props) {
  return (
    <div className="container">
      <div className="battleList">
        <Formik
          initialValues={{
            pokemon1: '',
            pokemon2: '',
            pokemon3: '',
            position1: 1,
            position2: 2,
            position3: 3,
          }}
          onSubmit={async (values) => {
            console.log('values', values);
            props.selectTeamProp(values);
          }}
        >
          <Form>
            <Field id="pokemon1" name="pokemon1" placeholder="pikachu" type="text" />
            <Field id="pokemon2" name="pokemon2" placeholder="eevee" type="text" />
            <Field id="pokemon3" name="pokemon3" placeholder="nidorina" type="text" />
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
SelectPkns.propTypes = {
  selectTeamProp: PropTypes.func,
};
const mapStateToProps = (state) => ({
  battle: state.battleR.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    selectTeamProp: (battleForm) => dispatch(selectTeamAction({ battleForm, id: 39 })),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(SelectPkns);
