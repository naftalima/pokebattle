import PropTypes from 'prop-types';
import React from 'react';

import Team from './Team';

export default function TeamPokemon({ trainerTeamPokemons }) {
  console.log('trainerTeamPokemons', typeof trainerTeamPokemons);
  return (
    <tr>
      {trainerTeamPokemons ? (
        <div>
          <Team pokemons={trainerTeamPokemons} />
        </div>
      ) : (
        <td>The team is empty. Waiting for the trainer to choose the Pokemons for the team.</td>
      )}
    </tr>
  );
}
TeamPokemon.propTypes = {
  trainerTeamPokemons: PropTypes.object,
};
