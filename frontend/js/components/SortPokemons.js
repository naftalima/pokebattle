/* eslint-disable babel/camelcase */
import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';
import { SortableContainer, arrayMove } from 'react-sortable-hoc';

import { selectTeamApi } from '../utils/api';

import PokemonList from './PokemonList';

const SortableList = SortableContainer(PokemonList);

function SortPokemons(props) {
  const { teamPokemons, teamId, history } = props;
  const [pokemons, setTodos] = useState(teamPokemons);

  const onSortEnd = ({ oldIndex, newIndex }) => {
    const newPokemons = arrayMove(pokemons, oldIndex, newIndex);
    setTodos(newPokemons);
  };

  return (
    <div>
      <SortableList axis="x" items={pokemons} onSortEnd={onSortEnd} />
      <h1>.</h1>
      <h1>.</h1>
      <h1>.</h1>
      <h1>.</h1>
      <button
        className="order-btn"
        type="submit"
        onClick={() => {
          const values = {
            pokemon_1: pokemons[0].name,
            pokemon_2: pokemons[1].name,
            pokemon_3: pokemons[2].name,
          };
          selectTeamApi({ teamId, values }).then(history.push('/v2/battle'));
        }}
      >
        Submit
      </button>
    </div>
  );
}
SortPokemons.propTypes = {
  teamPokemons: PropTypes.array,
  teamId: PropTypes.string,
  history: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { pokemons, teams } = state.battleR;
  const { teamId } = ownProps;

  const team = teams ? teams[teamId] : {};

  const teamPokemonsId = team ? team.pokemons : {};
  const teamPokemons = [];
  if (pokemons) {
    teamPokemonsId.map((pokemonId) => {
      // eslint-disable-next-line no-unused-vars
      for (const [key, value] of Object.entries(pokemons)) {
        if (value.id === pokemonId) {
          teamPokemons.push(value);
        }
      }
      return true;
    });
  }

  return { teamPokemons, teamId };
};

export default withRouter(connect(mapStateToProps)(SortPokemons));
