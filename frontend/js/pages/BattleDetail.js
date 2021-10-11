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
      battleId,
      creator,
      opponent,
      creatorTeamPokemons,
      opponentTeamPokemons,
      winner,
    } = this.props;
    if (battleId === null) {
      return (
        <div className="container">
          <div className="battleDetail">
            <h1>Its not a valid battle id</h1>
          </div>
        </div>
      );
    }
    return (
      <div className="container">
        <div className="battleDetail">
          <div className="battleDetail">
            <p className="title">Battle #{JSON.stringify(battleId)}</p>
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
                {creatorTeamPokemons ? (
                  <div>
                    <Team pokemons={creatorTeamPokemons} />
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
                {opponentTeamPokemons ? (
                  <div>
                    <Team pokemons={opponentTeamPokemons} />
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
}
BattleDetail.propTypes = {
  fetchBattle: PropTypes.func,
  battleId: PropTypes.number,
  creator: PropTypes.object,
  opponent: PropTypes.object,
  creatorTeamPokemons: PropTypes.array,
  opponentTeamPokemons: PropTypes.array,
  winner: PropTypes.object,
};

const mapStateToProps = (state) => {
  const { battleId, battle, pokemons, teams, users } = state.battleR;

  const creator = battle ? users[battle[battleId].creator] : null;
  const opponent = battle ? users[battle[battleId].opponent] : null;

  const battleTeam = battle ? battle[battleId].teams : [null, null];
  const [creatorTeamId, opponentTeamId] = battleTeam;

  const creatorTeamPokemonsId = creatorTeamId ? teams[creatorTeamId].pokemons : null;
  const opponentTeamPokemonsId = opponentTeamId ? teams[opponentTeamId].pokemons : null;

  const creatorTeamPokemons = creatorTeamPokemonsId
    ? creatorTeamPokemonsId.map((pokemonId) => pokemons[pokemonId])
    : null;
  const opponentTeamPokemons = opponentTeamPokemonsId
    ? opponentTeamPokemonsId.map((pokemonId) => pokemons[pokemonId])
    : null;

  const winner = battle ? (battle[battleId].winner ? users[battle[battleId].winner] : null) : null;

  return { battleId, creator, creatorTeamPokemons, opponent, opponentTeamPokemons, winner };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
