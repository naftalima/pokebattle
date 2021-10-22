import PropTypes from 'prop-types';
import React from 'react';

export default function PokemonNameList({ pokemons }) {
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
PokemonNameList.propTypes = {
  pokemons: PropTypes.object,
};
