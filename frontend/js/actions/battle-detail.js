import axios from 'axios';

const baseURL = `${window.location.protocol}//${window.location.host}`;

const BattleDetailtUrl = `${baseURL}/api/battle/`;

export const getBattleDetail = (id) => {
  return axios
    .get(`${BattleDetailtUrl}${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};
