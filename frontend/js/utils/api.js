/* eslint no-console: ["error", { allow: ["log"] }] */
import axios from 'axios';

const baseURL = `${window.location.protocol}//${window.location.host}`;
const BattleUrl = `${baseURL}/api/battle/`;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (const element of cookies) {
      const cookie = element.trim();
      if (cookie.slice(0, Math.max(0, name.length + 1)) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.slice(Math.max(0, name.length + 1)));
        break;
      }
    }
  }
  return cookieValue;
}

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

const csrftoken = getCookie('csrftoken');

export const createBattleApi = (battleForm) => {
  return axios
    .post(`${BattleUrl}new/`, battleForm, { headers: { 'X-CSRFToken': csrftoken } })
    .then((res) => {
      console.log('createBattleApi', battleForm);
      return res;
    })
    .catch((err) => {
      console.log(err);
    });
};
