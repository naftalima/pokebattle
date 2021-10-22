import PropTypes from 'prop-types';
import React from 'react';

export default function PokemonList({ pokemons }) {
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
