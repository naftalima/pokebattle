import { normalize } from 'normalizr';

import { getBattleDetailFromApi, getBattleListFromApi, createBattleApi } from '../utils/api';
import { battlesEntity, battleEntity } from '../utils/schema';

import { BATTLE_DETAIL, BATTLE_LIST, CREATE_BATTLE } from './actionsTypes';

export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    getBattleDetailFromApi(battleId).then((battle) => {
      const normalizedBattle = normalize(battle, battleEntity);
      return dispatch({ type: BATTLE_DETAIL, payload: normalizedBattle });
    });
}

export function getBattleListAction() {
  return (dispatch) =>
    getBattleListFromApi().then((battles) => {
      const normalizedBattles = normalize(battles, battlesEntity);
      return dispatch({ type: BATTLE_LIST, payload: normalizedBattles });
    });
}

export function createBattleAction(battleForm) {
  return (dispatch) =>
    createBattleApi(battleForm).then((battle) => {
      console.log('createBattleAction', battle);
      return dispatch({ type: CREATE_BATTLE, payload: battle });
    });
}
