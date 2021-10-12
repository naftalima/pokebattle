/* eslint-disable react/prop-types */
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import Team from '../components/Team';
import { getBattleDetailAction } from '../redux/actions';
// import { getUserName } from '../utils/format';

class BattleDetail extends React.Component {
  componentDidMount() {
    const { pathname } = window.location;
    const battleId = Number(pathname.split('/').pop());

    const { fetchBattle } = this.props;
    fetchBattle(battleId);
  }

  render() {
    const { battle } = this.props;

    console.log('BattleDetail1', battle);
    if (!battle.id) {
      return (
        <div className="container">
          <div className="battleDetail">
            <h1>Its not a valid battle id</h1>
          </div>
        </div>
      );
    }

    const battleTeam = battle ? battle.teams : [null, null];
    const [creatorTeamId, opponentTeamId] = battleTeam;
    console.log('BattleDetail2', battle);

    return (
      <div className="container">
        <div className="battleDetail">
          <div className="battleDetail">
            {/* <p className="title">Battle #{JSON.stringify(battleId)}</p> */}
            {/* <h4>
              <span className="trainer">{creator ? getUserName(creator.email) : ''}</span>{' '}
              challenged{' '}
              <span className="trainer">{opponent ? getUserName(opponent.email) : ''}</span>
            </h4> */}
            <Team trainerTeamId={creatorTeamId} />
            <Team trainerTeamId={opponentTeamId} />
            {/* {winner ? (
              <h1>
                And the winner is <span className="winner">{getUserName(winner.email)}</span>
              </h1>
            ) : (
              <h2>There is no winner yet</h2>
            )} */}
          </div>
        </div>
      </div>
    );
  }
}
BattleDetail.propTypes = {
  fetchBattle: PropTypes.func,
  // battleId: PropTypes.number,
  // creator: PropTypes.object,
  // opponent: PropTypes.object,
  // creatorTeamPokemons: PropTypes.array,
  // opponentTeamPokemons: PropTypes.array,
  // winner: PropTypes.object,
};

const mapStateToProps = (state) => {
  const { battles } = state.battleR;

  const { pathname } = window.location;
  const battleId = Number(pathname.split('/').pop());

  const battle = battles[battleId] ? battles[battleId] : {};

  // const creator = battle ? users[battle[battleId].creator] : null;
  // const opponent = battle ? users[battle[battleId].opponent] : null;

  // const battleTeam = battle ? battle[battleId].teams : [null, null];
  // const [creatorTeamId, opponentTeamId] = battleTeam;

  // const creatorTeamPokemonsId = creatorTeamId ? teams[creatorTeamId].pokemons : null;
  // const opponentTeamPokemonsId = opponentTeamId ? teams[opponentTeamId].pokemons : null;

  // const creatorTeamPokemons = creatorTeamPokemonsId
  //   ? creatorTeamPokemonsId.map((pokemonId) => pokemons[pokemonId])
  //   : null;
  // const opponentTeamPokemons = opponentTeamPokemonsId
  //   ? opponentTeamPokemonsId.map((pokemonId) => pokemons[pokemonId])
  //   : null;

  // const winner = battle ? (battle[battleId].winner ? users[battle[battleId].winner] : null) : null;

  // return { battleId, battle, winner };
  return { battle };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
