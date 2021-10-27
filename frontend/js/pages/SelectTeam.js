/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable babel/camelcase */
import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';

import FormPokemons from '../components/FormPokemons';
import Loading from '../components/Loading';
import SortPokemons from '../components/SortPokemons';
import { getPokemonListAction, getTeamDetailAction } from '../redux/actions';

function SelectTeam(props) {
  const { emptyPokemonTeam, emptyPokemonList, pokemons, fetchPokemons, fetchTeam, team } = props;
  const { id } = useParams();
  const teamId = id;
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
  return (
    <div className="container">
      <div className="battleList">
        {emptyPokemonTeam ? (
          <div>
            <h1 className="title">Choose your Team!</h1>
            <FormPokemons pokemons={pokemons} teamId={teamId} />
          </div>
        ) : (
          <div>
            <h1 className="title">Reorder your Team!</h1>
            <SortPokemons team={team} teamId={teamId} />
          </div>
        )}
      </div>
    </div>
  );
}
SelectTeam.propTypes = {
  pokemons: PropTypes.object,
  emptyPokemonList: PropTypes.bool,
  emptyPokemonTeam: PropTypes.bool,
  fetchPokemons: PropTypes.func,
  fetchTeam: PropTypes.func,
  team: PropTypes.object,
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
export default connect(mapStateToProps, mapDispatchToProps)(SelectTeam);
