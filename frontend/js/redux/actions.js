import { normalize } from 'normalizr';

import { getBattleDetailFromApi, getBattleListFromApi } from '../utils/api';
import { battlesEntity } from '../utils/schema';

import { BATTLE_DETAIL, BATTLE_LIST } from './actionsTypes';

export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    getBattleDetailFromApi(battleId).then((battle) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battle });
    });
}

export function getBattleListAction() {
  return (dispatch) =>
    getBattleListFromApi().then((battles) => {
      const normalizedBattles = normalize(battles, battlesEntity);
      return dispatch({ type: BATTLE_LIST, payload: normalizedBattles });
    });
}
