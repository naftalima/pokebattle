import axios from 'axios';

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
