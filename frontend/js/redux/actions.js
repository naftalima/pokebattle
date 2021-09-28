// eslint-disable-next-line import/no-cycle
import { getBattleDetailFromApi } from '../utils/api';

export const BATTLE_DETAIL = 'BATTLE_DETAIL';

// export const getBattleDetailAction = (battles) => ({
//   type: BATTLE_DETAIL,
//   payload: battles,
// });
export function getBattleDetailAction(battleId) {
  return (dispatch) =>
    getBattleDetailFromApi(battleId).then((battle) => {
      return dispatch({ type: BATTLE_DETAIL, payload: battle });
    });
}
