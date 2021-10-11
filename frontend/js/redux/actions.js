import { getBattleDetailFromApi } from '../utils/api';

export const BATTLE_DETAIL = 'BATTLE_DETAIL';

export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    getBattleDetailFromApi(battleId).then((battle) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battle });
    });
}
