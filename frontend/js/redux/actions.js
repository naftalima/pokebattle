import { normalize } from 'normalizr';

import * as api from '../utils/api';
import { battlesEntity, battleEntity } from '../utils/schema';

import * as actionsTypes from './actionsTypes';

export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    api.getBattleDetailFromApi(battleId).then((battle) => {
      const normalizedBattle = normalize(battle, battleEntity);
      return dispatch({ type: actionsTypes.BATTLE_DETAIL, payload: normalizedBattle });
    });
}

export function getBattleListAction() {
  return (dispatch) =>
    api.getBattleListFromApi().then((battles) => {
      const normalizedBattles = normalize(battles, battlesEntity);
      return dispatch({ type: actionsTypes.BATTLE_LIST, payload: normalizedBattles });
    });
}

export function getPokemonListAction() {
  return (dispatch) =>
    api.getPokemonListFromApi().then((pokemons) => {
      return dispatch({ type: actionsTypes.POKEMON_LIST, payload: pokemons });
    });
}

export function selectTeamAction(payload) {
  return (dispatch) =>
    api.selectTeamApi(payload).then((team) => {
      return dispatch({ type: actionsTypes.SELECT_TEAM, payload: team });
    });
}
