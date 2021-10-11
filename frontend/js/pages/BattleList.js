import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import Battles from '../components/Battles';
import { getBattleListAction } from '../redux/actions';

class BattleList extends React.Component {
  componentDidMount() {
    const { fetchBattles } = this.props;
    fetchBattles();
  }

  render() {
    const {
      battleList: { battles },
    } = this.props;

    const isFinished = (battle) => battle.winner !== null;
    const finishedBattles = battles ? battles.filter(isFinished) : {};
    const isUnfinished = (battle) => battle.winner === null;
    const unfinishedBattles = battles ? battles.filter(isUnfinished) : {};

    if (battles !== null) {
      return (
        <div className="container">
          <div className="battleList">
            <table>
              <tr>
                <td className="title">On going Battles</td>
                <td className="title">Settled Battles</td>
              </tr>
              <tr>
                <td>
                  {unfinishedBattles ? (
                    <Battles battles={unfinishedBattles} />
                  ) : (
                    <td>Sorry, no battles in this list.</td>
                  )}
                </td>
                <td>
                  {finishedBattles ? (
                    <Battles battles={finishedBattles} />
                  ) : (
                    <td>Sorry, no battles in this list.</td>
                  )}
                </td>
              </tr>
            </table>
          </div>
        </div>
      );
    }
    return (
      <div className="container">
        <div className="battleList">
          <h1>Sorry, no battles in this list.</h1>
        </div>
      </div>
    );
  }
}
BattleList.propTypes = {
  battleList: PropTypes.object,
  fetchBattles: PropTypes.func,
};

const mapStateToProps = (state) => ({
  battleList: state.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattles: () => dispatch(getBattleListAction()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleList);
