import { getBattleDetailFromApi, getBattleListFromApi } from '../utils/api';

export const BATTLE_DETAIL = 'BATTLE_DETAIL';
export const BATTLE_LIST = 'BATTLE_LIST';

export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    getBattleDetailFromApi(battleId).then((battle) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battle });
    });
}

export function getBattleListAction() {
  return (dispatch) =>
    getBattleListFromApi().then((battles) => {
      return dispatch({ type: BATTLE_LIST, payload: battles });
    });
}
