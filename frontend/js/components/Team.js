import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getUserName } from '../utils/format';

import Pokemons from './Pokemon';

function Team({ trainer, pokemonsId }) {
  return (
    <div className="team">
      <table>
        <tr>
          <th>
            <span className="trainer">{getUserName(trainer.email)}</span>&apos;s Team is:
          </th>
        </tr>
        <tr>
          {pokemonsId.length === 0 ? (
            <td>The team is empty. Waiting for the trainer to choose the Pokemons for the team.</td>
          ) : (
            pokemonsId.map((pokemonId) => <Pokemons key={pokemonId} pokemonId={pokemonId} />)
          )}
        </tr>
      </table>
    </div>
  );
}
Team.propTypes = {
  trainer: PropTypes.object,
  pokemonsId: PropTypes.array,
};

const mapStateToProps = (state, ownProps) => {
  const { teams, users } = state.battleR;
  const { trainerTeamId } = ownProps;

  const team = trainerTeamId ? teams[trainerTeamId] : {};

  const trainer = team ? users[team.trainer] : {};
  const pokemonsId = team ? team.pokemons : [];

  return { trainer, pokemonsId };
};

export default connect(mapStateToProps)(Team);
