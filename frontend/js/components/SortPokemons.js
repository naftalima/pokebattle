/* eslint-disable babel/camelcase */
import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { connect } from 'react-redux';
import { SortableContainer, arrayMove } from 'react-sortable-hoc';

import ToDoList from './ToDoList';

const SortableList = SortableContainer(ToDoList);

function SortPokemons({ teamPokemons }) {
  const [pokemons, setTodos] = useState(teamPokemons);

  const onSortEnd = ({ oldIndex, newIndex }) => {
    const newPokemons = arrayMove(pokemons, oldIndex, newIndex);
    setTodos(newPokemons);
  };

  return (
    <div className="container">
      <div className="battleList">
        <h1>select the order your pokemons will battle:</h1>
        <SortableList axis="y" items={pokemons} onSortEnd={onSortEnd} />
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
