import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

// import { fetchBattleDetail } from '../utils/api';
import { getBattleDetailAction } from '../redux/actions';
import './BattleDetail.scss';

function Team({ pokemons }) {
  const teamPokemon = [];
  for (const pokemon of pokemons) {
    teamPokemon.push(
      <td key={pokemon.id}>
        <img alt={pokemon} src={pokemon.img_url} /> {pokemon.name}
      </td>
    );
  }
  return (
    <table>
      <tbody>
        <tr>{teamPokemon}</tr>
      </tbody>
    </table>
  );
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
                <h1>Battle #{JSON.stringify(battle.id)}</h1>
                <p>Created at {JSON.stringify(battle.created_at)}</p>
                <p>
                  <strong>{battle.creator ? battle.creator.email : ''}</strong> challenged{' '}
                  <strong>{battle.opponent ? battle.opponent.email : ''}</strong>
                </p>
                {battle.teams[0].pokemons.length > 0 ? (
                  <div>
                    <p>{battle.creator.email} Team is:</p>
                    <Team pokemons={battle.teams[0].pokemons} />
                  </div>
                ) : (
                  <p>Your team is empty. Choose Pokemons for your team.</p>
                )}
                {battle.teams[1].pokemons.length > 0 ? (
                  <div>
                    <p>{battle.opponent.email} Team is:</p>
                    <Team pokemons={battle.teams[1].pokemons} />
                  </div>
                ) : (
                  <p>Wait for your opponent to choose their team.</p>
                )}
                {battle.winner ? (
                  <p>And the winner is {battle.winner.email}</p>
                ) : (
                  <p>There is no winner yet</p>
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
  // battle: PropTypes.object,
  battleDetail: PropTypes.object,
  fetchBattle: PropTypes.func,
};

const mapStateToProps = (state) => ({
  battleDetail: state.battle,
});

// const mapDispatchToProps = (dispatch) => {
//   return { fetchBattle: (id) => fetchBattleDetail(id, dispatch) };
// };
const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
