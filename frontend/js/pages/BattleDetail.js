import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import Team from '../components/Team';
import { getBattleDetailAction } from '../redux/actions';
import { getUserName } from '../utils/format';

class BattleDetail extends React.Component {
  componentDidMount() {
    const { pathname } = window.location;
    const battleId = Number(pathname.split('/').pop());

    const { fetchBattle } = this.props;
    fetchBattle(battleId);
  }

  render() {
    const {
      battleDetail: { battle },
    } = this.props;

    if (battle !== null) {
      const { creator, opponent, teams, winner } = battle;
      const creatorTeam = teams[0];
      const opponentTeam = teams[1];

      return (
        <div className="container">
          <div className="battleDetail">
            <div className="battleDetail">
              <p className="title">Battle #{JSON.stringify(battle.id)}</p>
              <h4>
                <span className="trainer">{creator ? getUserName(creator.email) : ''}</span>{' '}
                challenged{' '}
                <span className="trainer">{opponent ? getUserName(opponent.email) : ''}</span>
              </h4>
              <table>
                <tr>
                  <th>
                    <span className="trainer">{getUserName(creator.email)}</span>&apos;s Team is:
                  </th>
                </tr>
                <tr>
                  {creatorTeam.pokemons.length ? (
                    <div>
                      <Team pokemons={creatorTeam.pokemons} />
                    </div>
                  ) : (
                    <td>Your team is empty. Choose Pokemons for your team.</td>
                  )}
                </tr>
              </table>
              <table>
                <tr>
                  <th>
                    <span className="trainer">{getUserName(opponent.email)}</span>&apos;s Team is:
                  </th>
                </tr>
                <tr>
                  {opponentTeam.pokemons.length ? (
                    <div>
                      <Team pokemons={opponentTeam.pokemons} />
                    </div>
                  ) : (
                    <td>Wait for your opponent to choose their team.</td>
                  )}
                </tr>
              </table>

              {winner ? (
                <h1>
                  And the winner is <span className="winner">{getUserName(winner.email)}</span>
                </h1>
              ) : (
                <h2>There is no winner yet</h2>
              )}
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="container">
        <div className="battleDetail">
          <h1>Its not a valid battle id</h1>
        </div>
      </div>
    );
  }
}
BattleDetail.propTypes = {
  battleDetail: PropTypes.object,
  fetchBattle: PropTypes.func,
};

const mapStateToProps = (state) => ({
  battleDetail: state.battle,
});

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
