import axios from 'axios';

// import { getBattleDetailAction } from '../redux/actions';

const baseURL = `${window.location.protocol}//${window.location.host}`;

const BattleDetailtUrl = `${baseURL}/api/battle/`;

export const getBattleDetailFromApi = (id) => {
  return axios
    .get(`${BattleDetailtUrl}${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      /* eslint no-console: ["error", { allow: ["log"] }] */
      console.log(err);
    });
};

// export function fetchBattleDetail(battleId) {
//   console.log('fetchBattleDetail(battleId)');
//   return (dispatch) => {
//     console.log('dispatch');
//     const response = getBattleDetailFromApi(battleId);
//     return dispatch(getBattleDetailAction({ type: 'BATTLE_DETAIL', payload: response }));
//   };
// }
