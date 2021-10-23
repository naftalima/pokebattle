/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { selectTeamApi } from '../utils/api';

import PokemonNameList from './PokemonNameList';

function FormPokemons(props) {
  const { teamId, history, pokemons } = props;

  return (
    <Formik
      initialValues={{
        pokemon_1: '',
        pokemon_2: '',
        pokemon_3: '',
      }}
      onSubmit={async (values) => {
        selectTeamApi({ teamId, values }).then(history.go(0));
      }}
    >
      <Form>
        <div className="form">
          <div>
            <label htmlFor="pokemon">Pokemon:</label>
            <Field id="pokemon_1" list="pokemons" name="pokemon_1" type="text" />
          </div>
          <PokemonNameList pokemons={pokemons} />
          <div>
            <label htmlFor="pokemon">Pokemon:</label>
            <Field id="pokemon_2" list="pokemons" name="pokemon_2" type="text" />
          </div>
          <PokemonNameList pokemons={pokemons} />
          <div>
            <label htmlFor="pokemon">Pokemon:</label>
            <Field id="pokemon_3" list="pokemons" name="pokemon_3" type="text" />
          </div>
          <PokemonNameList pokemons={pokemons} />
          <button className="battle-id-btn" type="submit">
            Submit
          </button>
        </div>
      </Form>
    </Formik>
  );
}
FormPokemons.propTypes = {
  pokemons: PropTypes.object,
  teamId: PropTypes.string,
  history: PropTypes.object,
};

const mapStateToProps = (_state, ownProps) => {
  const { teamId, pokemons } = ownProps;

  return { teamId, pokemons };
};

export default withRouter(connect(mapStateToProps)(FormPokemons));
