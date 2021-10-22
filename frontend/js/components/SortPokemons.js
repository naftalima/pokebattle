/* eslint-disable babel/camelcase */
import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { connect } from 'react-redux';
import { SortableContainer, arrayMove } from 'react-sortable-hoc';

import PokemonList from './PokemonList';

const SortableList = SortableContainer(PokemonList);

function SortPokemons({ teamPokemons }) {
  const [pokemons, setTodos] = useState(teamPokemons);

  const onSortEnd = ({ oldIndex, newIndex }) => {
    const newPokemons = arrayMove(pokemons, oldIndex, newIndex);
    setTodos(newPokemons);
    console.log(newPokemons);
  };

  return (
    <div className="container">
      <div className="battleList">
        <h3>select the order your pokemons will battle:</h3>
        <SortableList axis="x" items={pokemons} onSortEnd={onSortEnd} />
        <h1>.</h1>
        <h1>.</h1>
        <h1>.</h1>
        <h1>.</h1>
        <button className="order-btn" type="submit">
          Submit
        </button>
      </div>
    </div>
  );
}
SortPokemons.propTypes = {
  teamPokemons: PropTypes.array,
};

const mapStateToProps = (state, ownProps) => {
  const { pokemons } = state.battleR;
  const { team } = ownProps;

  const teamPokemonsId = team ? team.pokemons : {};
  const teamPokemons = pokemons ? teamPokemonsId.map((pokemonId) => pokemons[pokemonId]) : [];

  return { teamPokemons };
};

export default connect(mapStateToProps)(SortPokemons);
