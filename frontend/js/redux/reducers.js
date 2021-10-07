import { combineReducers } from 'redux';

import * as actionsTypes from './actionsTypes';

const initialState = {
  battle: null,
  battleId: null,
  battles: null,
  battlesId: null,
  pokemons: null,
  teams: null,
  users: null,
};

const battleReducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case actionsTypes.BATTLE_DETAIL:
      return {
        ...state,
        battleId: action.payload.result,
        battle: action.payload.entities.battle,
        pokemons: action.payload.entities.pokemon,
        teams: action.payload.entities.team,
        users: action.payload.entities.users,
      };
    case actionsTypes.BATTLE_LIST:
      return {
        ...state,
        battles: action.payload.entities.battle,
        battleIds: action.payload.result,
      };
    case actionsTypes.CREATE_BATTLE:
      return {
        ...state,
        battle: action.payload,
      };
    default:
      return state;
  }
};

export const rootReducer = combineReducers({
  battleR: battleReducer,
});
