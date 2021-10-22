/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable babel/camelcase */
import { Formik, Field, Form } from 'formik';
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import Loading from '../components/Loading';
import PokemonNameList from '../components/PokemonNameList';
import SortPokemons from '../components/SortPokemons';
import { getPokemonListAction, getTeamDetailAction } from '../redux/actions';
import { selectTeamApi } from '../utils/api';

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
    return <Loading />;
  }
  if (emptyPokemonTeam) {
    return (
      <div className="container">
        <div className="battleList">
          <h1 className="title">Choose your Team!</h1>
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
        </div>
      </div>
    );
  }
  return <SortPokemons team={team} />;
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
