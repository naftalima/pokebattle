/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import PokemonCard from '../components/PokemonCard';
import { getPokemonListAction, getTeamDetailAction } from '../redux/actions';
import { selectTeamApi } from '../utils/api';

function PokemonList({ pokemons }) {
  return (
    <datalist id="pokemons">
      {pokemons.map((pokemon) => {
        return (
          <option key={pokemon.id} value={pokemon.name}>
            {`${pokemon.name}`}
          </option>
        );
      })}
    </datalist>
  );
}
PokemonList.propTypes = {
  pokemons: PropTypes.object,
};

function SelectTeam(props) {
  const {
    match: { params },
    fetchTeam,
    team,
    emptyPokemonList,
    pokemons,
    fetchPokemons,
    emptyPokemonTeam,
  } = props;

  const teamId = params.id;
  useEffect(() => {
    if (team && team.id !== Number(teamId)) {
      fetchTeam(teamId);
    }
  });

  useEffect(() => {
    if (emptyPokemonList) {
      fetchPokemons();
    }
  });

  if (emptyPokemonList) {
    return (
      <div className="container">
        <div className="battleList">
          <h1>LOADING</h1>
        </div>
      </div>
    );
  }
  if (emptyPokemonTeam) {
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
              <PokemonList pokemons={pokemons} />
              <Field id="pokemon_2" list="pokemons" name="pokemon_2" type="text" />
              <PokemonList pokemons={pokemons} />
              <Field id="pokemon_3" list="pokemons" name="pokemon_3" type="text" />
              <PokemonList pokemons={pokemons} />
              <button type="submit">Submit</button>
            </Form>
          </Formik>
        </div>
      </div>
    );
  }
  return (
    <div className="container">
      <div className="battleList">
        <h1>Team Pokemon</h1>
        <PokemonCard pokemonId={team.pokemons[0]} />
        <PokemonCard pokemonId={team.pokemons[1]} />
        <PokemonCard pokemonId={team.pokemons[2]} />
      </div>
    </div>
  );
}
SelectTeam.propTypes = {
  history: PropTypes.object,
  pokemons: PropTypes.object,
  emptyPokemonList: PropTypes.bool,
  emptyPokemonTeam: PropTypes.bool,
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
  const pokemonTeam = team ? team.pokemons : [];
  const emptyPokemonTeam = pokemonTeam ? pokemonTeam.length === 0 : true;
  const emptyPokemonList = Object.keys(pokemons).length === 0 && pokemons.constructor === Object;

  return { team, pokemons, emptyPokemonList, emptyPokemonTeam };
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
