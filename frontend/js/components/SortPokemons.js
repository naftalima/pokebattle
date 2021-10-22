/* eslint-disable babel/camelcase */
// import arrayMove from 'array-move';
import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { connect } from 'react-redux';
import { SortableContainer, arrayMove } from 'react-sortable-hoc';

import PokemonCard from './PokemonCard';
import ToDoList from './ToDoList';

const todosInit = [
  { id: 1, content: 'content 1', isDone: false },
  { id: 2, content: 'content 2', isDone: false },
  { id: 3, content: 'content 3', isDone: false },
];
const SortableList = SortableContainer(ToDoList);

function SortPokemons({ pokemon_1, pokemon_2, pokemon_3 }) {
  const [todos, setTodos] = useState(todosInit);

  const onSortEnd = (e) => {
    const newTodos = arrayMove(todos, e.oldIndex, e.newIndex);
    setTodos(newTodos);
  };

  return (
    <div className="container">
      <div className="battleList">
        <h1>Ordene seus pokemons</h1>
        <SortableList items={todos} onSortEnd={onSortEnd} />
        <h1>Team Pokemon</h1>
        <PokemonCard pokemonId={pokemon_1} />
        <PokemonCard pokemonId={pokemon_2} />
        <PokemonCard pokemonId={pokemon_3} />
      </div>
    </div>
  );
}
SortPokemons.propTypes = {
  pokemon_1: PropTypes.number,
  pokemon_2: PropTypes.number,
  pokemon_3: PropTypes.number,
};

const mapStateToProps = (_state, ownProps) => {
  const { team } = ownProps;

  const pokemon_1 = team ? team.pokemons[0] : {};
  const pokemon_2 = team ? team.pokemons[1] : {};
  const pokemon_3 = team ? team.pokemons[2] : {};

  return { pokemon_1, pokemon_2, pokemon_3 };
};

export default connect(mapStateToProps)(SortPokemons);
