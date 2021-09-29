import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getBattleDetailAction } from '../redux/actions';
import { getUserName } from '../utils/format';

function Team({ pokemons }) {
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
      return (
        <div>
          <img
            alt="pokemon"
            className="pokebattle-logo"
            src="https://team-rocket-blasting-off-again.github.io/pokebattle/assets/pokebattle-title.png"
          />
          <div className="container">
            <div className="battleDetail">
              <div className="battleDetail">
                <p className="title">Battle #{JSON.stringify(battle.id)}</p>
                <h4>
                  <span className="trainer">
                    {battle.creator ? getUserName(battle.creator.email) : ''}
                  </span>{' '}
                  challenged{' '}
                  <span className="trainer">
                    {battle.opponent ? getUserName(battle.opponent.email) : ''}
                  </span>
                </h4>
                <table>
                  <tr>
                    <th>
                      <span className="trainer">{getUserName(battle.creator.email)}</span>&apos;s
                      Team is:
                    </th>
                  </tr>
                  <tr>
                    {battle.teams[0].pokemons.length > 0 ? (
                      <div>
                        <Team pokemons={battle.teams[0].pokemons} />
                      </div>
                    ) : (
                      <td>Your team is empty. Choose Pokemons for your team.</td>
                    )}
                  </tr>
                </table>
                <table>
                  <tr>
                    <th>
                      <span className="trainer">{getUserName(battle.opponent.email)}</span>&apos;s
                      Team is:
                    </th>
                  </tr>
                  <tr>
                    {battle.teams[1].pokemons.length > 0 ? (
                      <div>
                        <Team pokemons={battle.teams[1].pokemons} />
                      </div>
                    ) : (
                      <td>Wait for your opponent to choose their team.</td>
                    )}
                  </tr>
                </table>

                {battle.winner ? (
                  <h1>
                    And the winner is{' '}
                    <span className="winner">{getUserName(battle.winner.email)}</span>
                  </h1>
                ) : (
                  <h2>There is no winner yet</h2>
                )}
              </div>
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
          <div className="battleDetail">
            <h1>Its not a valid battle id</h1>
          </div>
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
