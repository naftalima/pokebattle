import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getUserName } from '../utils/format';

import Pokemons from './Pokemons';

function Team({ trainer, trainerTeamId }) {
  return (
    <div className="team">
      {trainerTeamId === null ? (
        <table>
          <tr>
            <th>there is no team</th>
          </tr>
        </table>
      ) : (
        <table>
          <tr>
            <th>
              <span className="trainer">{getUserName(trainer.email)}</span>&apos;s Team is:
            </th>
          </tr>
          <tr>
            <Pokemons trainerTeamId={trainerTeamId} />
          </tr>
        </table>
      )}
    </div>
  );
}
Team.propTypes = {
  trainer: PropTypes.object,
  trainerTeamId: PropTypes.number,
};

const mapStateToProps = (state, ownProps) => {
  const { teams, users } = state.battleR;
  const { trainerTeamId } = ownProps;

  const team = teams ? teams[trainerTeamId] : {};
  const trainerId = team ? team.trainer : {};
  const trainer = users ? users[trainerId] : {};

  return { trainer, trainerTeamId };
};

export default connect(mapStateToProps)(Team);
