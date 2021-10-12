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

export function createBattleAction(battleForm) {
  return (dispatch) =>
    api.createBattleApi(battleForm).then((battle) => {
      return dispatch({ type: actionsTypes.CREATE_BATTLE, payload: battle });
    });
}

export function selectTeamAction(teamForm) {
  return (dispatch) =>
    api.selectTeamApi(teamForm).then((team) => {
      return dispatch({ type: actionsTypes.SELECT_TEAM, payload: team });
    });
}
