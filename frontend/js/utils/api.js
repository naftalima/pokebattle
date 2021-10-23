/* eslint-disable babel/camelcase */
/* eslint no-console: ["error", { allow: ["log"] }] */
import axios from 'axios';

import getCookie from './cookie';

const csrftoken = getCookie('csrftoken');

const baseURL = `${window.location.protocol}//${window.location.host}`;
const battleUrl = `${baseURL}/api/battle/`;
const pokemonUrl = `${baseURL}/api/pokemon/`;
const createBattleUrl = `${battleUrl}new/`;
const selectTeamUrl = `${baseURL}/api/team/`;

export const getBattleDetailFromApi = (id) => {
  return axios
    .get(`${battleUrl}${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const getTeamDetailFromApi = (id) => {
  return axios
    .get(`${selectTeamUrl}${id}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const getBattleListFromApi = () => {
  return axios
    .get(`${battleUrl}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const getPokemonListFromApi = () => {
  return axios
    .get(`${pokemonUrl}`)
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const createBattleApi = (battleForm) => {
  return axios
    .post(`${createBattleUrl}`, battleForm, { headers: { 'X-CSRFToken': csrftoken } })
    .then((res) => {
      return res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

export const selectTeamApi = (payload) => {
  const { teamId, values } = payload;
  const team = {
    ...values,
    position_1: 1,
    position_2: 2,
    position_3: 3,
  };
  return axios
    .put(`${selectTeamUrl}${teamId}/edit/`, team, { headers: { 'X-CSRFToken': csrftoken } })
    .then((res) => {
      return res;
    })
    .catch((err) => {
      console.log(err);
    });
};
