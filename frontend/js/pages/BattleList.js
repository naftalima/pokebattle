import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';

import Battles from '../components/Battles';
import { getBattleListAction } from '../redux/actions';

function BattleList(props) {
  const { finishedBattles, unfinishedBattles, battleIds, fetchBattles } = props;

  useEffect(() => {
    fetchBattles();
  });

  if (battleIds === null) {
    return (
      <div className="container">
        <div className="battleList">
          <h1>Sorry, no battles yet.</h1>
        </div>
      </div>
    );
  }
  return (
    <div className="container">
      <div className="battleList">
        <table>
          <tr>
            <td className="title">On going Battles</td>
            <td className="title">Settled Battles</td>
          </tr>
          <tr>
            <Battles battles={unfinishedBattles} />
            <Battles battles={finishedBattles} />
          </tr>
        </table>
      </div>
    </div>
  );
}
BattleList.propTypes = {
  finishedBattles: PropTypes.array,
  unfinishedBattles: PropTypes.array,
  fetchBattles: PropTypes.func,
  battleIds: PropTypes.array,
};

const mapStateToProps = (state) => {
  const { battleIds, battles } = state.battleR;

  const battleList = battleIds ? battleIds.map((id) => battles[id]) : [];

  const isFinished = (battle) => battle.winner !== null;
  const isUnfinished = (battle) => battle.winner === null;

  const finishedBattles = battleList ? battleList.filter(isFinished) : [];
  const unfinishedBattles = battleList ? battleList.filter(isUnfinished) : [];

  return {
    finishedBattles,
    unfinishedBattles,
    battleIds,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattles: () => dispatch(getBattleListAction()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
