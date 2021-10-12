import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

function Pokemons({ trainerTeamPokemons }) {
  return (
    <tr>
      {trainerTeamPokemons.map((pokemon) => (
        <td key={pokemon.id} className="battle-detail-td">
          <div className="battle-detail-block">
            <div className="battle-datail-display">
              <img alt={pokemon} height="90px" src={pokemon.img_url} />
            </div>
            <div className="battle-detail-pokemon-name">{pokemon.name}</div>
          </div>
        </td>
      ))}
    </tr>
  );
}
Pokemons.propTypes = {
  trainerTeamPokemons: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { teams, pokemons } = state.battleR;
  const { trainerTeamId } = ownProps;

  const trainerTeamPokemonsId = trainerTeamId ? teams[trainerTeamId].pokemons : null;

  const trainerTeamPokemons = trainerTeamPokemonsId
    ? trainerTeamPokemonsId.map((pokemonId) => pokemons[pokemonId])
    : null;
  return { trainerTeamPokemons };
};

export default connect(mapStateToProps)(Pokemons);
