import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { getBattleListAction } from '../redux/actions';

import './BattleList.scss';

function Battles({ battles }) {
  const battleList = battles.map((battle) => {
    return (
      <tr key={battle.id} className="battle-id-btn">
        <Link to={{ pathname: `/v2/battle/${battle.id}` }}>Battle #{battle.id}</Link>
      </tr>
    );
  });
  return (
    <table>
      <td>{battleList}</td>
    </table>
  );
}
Battles.propTypes = {
  battles: PropTypes.array,
};

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
        <div>
          <img
            alt="pokemon"
            className="pokebattle-logo"
            src="https://team-rocket-blasting-off-again.github.io/pokebattle/assets/pokebattle-title.png"
          />
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
                      <h1>Sorry, no battles in this list.</h1>
                    )}
                  </td>
                  <td>
                    {finishedBattles ? (
                      <Battles battles={finishedBattles} />
                    ) : (
                      <h1>Sorry, no battles in this list.</h1>
                    )}
                  </td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div>
        <img
          alt="pokemon"
          className="pokebattle-logo"
          src="https://team-rocket-blasting-off-again.github.io/pokebattle/assets/pokebattle-title.png"
        />
        <div className="container">
          <div className="battleList">
            <h1>Sorry, no battles in this list.</h1>
          </div>
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
