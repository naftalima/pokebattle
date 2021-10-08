/* eslint no-console: ["error", { allow: ["log"] }] */
import axios from 'axios';

const baseURL = `${window.location.protocol}//${window.location.host}`;
const BattleUrl = `${baseURL}/api/battle/`;

export const getBattleDetailFromApi = (id) => {
  return axios
    .get(`${BattleUrl}${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const getBattleListFromApi = () => {
  return axios
    .get(`${BattleUrl}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const createBattleApi = (battleForm) => {
  return axios
    .post(`${BattleUrl}new/`, battleForm)
    .then((res) => {
      console.log('createBattleApi', battleForm);
      return res;
    })
    .catch((err) => {
      console.log(err);
    });
};
