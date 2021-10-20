/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { getPokemonListAction, getTeamDetailAction } from '../redux/actions';
import { selectTeamApi } from '../utils/api';

function PokemonList({ pokemonNames }) {
  return (
    <datalist id="pokemons">
      {pokemonNames.map((pokemon) => {
        return (
          <option key={pokemon} value={pokemon}>
            {`${pokemon}`}
          </option>
        );
      })}
    </datalist>
  );
}
PokemonList.propTypes = {
  pokemonNames: PropTypes.array,
};

function SelectTeam(props) {
  const {
    match: { params },
    fetchTeam,
    team,
    pokemonNames,
    fetchPokemons,
  } = props;

  const teamId = params.id;
  useEffect(() => {
    if (team && team.id === teamId) {
      fetchTeam(teamId);
    }
  });

  useEffect(() => {
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
            <PokemonList pokemonNames={pokemonNames} />
            <Field id="pokemon_2" list="pokemons" name="pokemon_2" type="text" />
            <PokemonList pokemonNames={pokemonNames} />
            <Field id="pokemon_3" list="pokemons" name="pokemon_3" type="text" />
            <PokemonList pokemonNames={pokemonNames} />
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
  fetchTeam: PropTypes.func,
  team: PropTypes.object,
  match: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { pokemons, teams } = state.battleR;
  const {
    match: { params },
  } = ownProps;
  const teamId = params.id;

  const team = teams ? teams[teamId] : {};

  const pokemonNames = [];
  if (pokemons) {
    // eslint-disable-next-line no-unused-vars
    for (const [key, value] of Object.entries(pokemons)) {
      pokemonNames.push(value.name);
    }
  }
  return { pokemonNames, team };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchPokemons: () => {
      dispatch(getPokemonListAction());
    },
    fetchTeam: (id) => dispatch(getTeamDetailAction(id)),
  };
};
export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SelectTeam));
