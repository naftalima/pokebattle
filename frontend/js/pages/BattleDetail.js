import PropTypes from 'prop-types';
import React from 'react';

import { getBattleDetail } from '../actions/battle-detail';
import './BattleDetail.scss';

function Team({ pokemons }) {
  const pokemonrows = [];
  for (const pokemon of pokemons) {
    pokemonrows.push(
      <td key={pokemon}>
        <img alt={pokemon} src={pokemon.img_url} /> {pokemon.name}
      </td>
    );
  }
  return (
    <table>
      <tr>{pokemonrows}</tr>
    </table>
  );
}

Team.propTypes = {
  pokemons: PropTypes.object.isRequired,
};

export default class BattleDetail extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      battle: null,
    };
  }

  componentDidMount() {
    const { pathname } = window.location;
    const battleId = Number(pathname.split('/').pop());

    getBattleDetail(battleId).then((data) => {
      this.setState({
        battle: data,
      });
      return null;
    });
  }

  render() {
    const { battle } = this.state;

    if (battle) {
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
                  <strong>{battle.creator.email}</strong> challenged{' '}
                  <strong>{battle.opponent.email}</strong>
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
