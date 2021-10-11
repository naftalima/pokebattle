import PropTypes from 'prop-types';
import React from 'react';

export default function Team({ pokemons }) {
  const teamPokemon = [];
  for (const pokemon of pokemons) {
    teamPokemon.push(
      <td key={pokemon.id} className="battle-detail-td">
        <div className="battle-detail-block">
          <div className="battle-datail-display">
            <img alt={pokemon} height="90px" src={pokemon.img_url} />
          </div>
          <div className="battle-detail-pokemon-name">{pokemon.name}</div>
        </div>
      </td>
    );
  }
  return teamPokemon;
}
Team.propTypes = {
  pokemons: PropTypes.array.isRequired,
};
