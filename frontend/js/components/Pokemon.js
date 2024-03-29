import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

function Pokemon({ pokemon }) {
  return (
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
Pokemon.propTypes = {
  pokemon: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { pokemons } = state.battleR;
  const { pokemonId } = ownProps;

  const pokemon = pokemonId ? pokemons[pokemonId] : {};

  return { pokemon };
};

export default connect(mapStateToProps)(Pokemon);
