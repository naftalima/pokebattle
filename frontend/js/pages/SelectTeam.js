/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { getPokemonListAction } from '../redux/actions';
import { selectTeamApi } from '../utils/api';

function SelectTeam(props) {
  const {
    match: { params },
    pokemonNames,
  } = props;

  const teamId = params.id;
  useEffect(() => {
    const { fetchPokemons, pokemonNames } = props;
    if (pokemonNames.length === 0) {
      fetchPokemons();
    }
  });

  if (pokemonNames.length === 0) {
    return <p>loading</p>;
  }
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
            selectTeamApi({ teamId, values });
            props.history.push('/v2/battle');
          }}
        >
          <Form>
            <Field id="pokemon_1" list="pokemons" name="pokemon_1" type="text" />
            <datalist id="pokemons">
              {pokemonNames.map((pokemon) => {
                return (
                  <option key={pokemon} value={pokemon}>
                    {`${pokemon}`}
                  </option>
                );
              })}
            </datalist>
            <Field id="pokemon_2" list="pokemons" name="pokemon_2" type="text" />
            <datalist id="pokemons">
              {pokemonNames.map((pokemon) => {
                return (
                  <option key={pokemon} value={pokemon}>
                    {`${pokemon}`}
                  </option>
                );
              })}
            </datalist>
            <Field id="pokemon_3" list="pokemons" name="pokemon_3" type="text" />
            <datalist id="pokemons">
              {pokemonNames.map((pokemon) => {
                return (
                  <option key={pokemon} value={pokemon}>
                    {`${pokemon}`}
                  </option>
                );
              })}
            </datalist>
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
SelectTeam.propTypes = {
  history: PropTypes.object,
  pokemonNames: PropTypes.array,
  fetchPokemons: PropTypes.func,
  match: PropTypes.object,
};

const mapStateToProps = (state) => {
  const { pokemons } = state.battleR;
  const pokemonNames = [];
  if (pokemons) {
    // eslint-disable-next-line no-unused-vars
    for (const [key, value] of Object.entries(pokemons)) {
      pokemonNames.push(value.name);
    }
  }
  return { pokemonNames };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchPokemons: () => {
      dispatch(getPokemonListAction());
    },
  };
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SelectTeam));
