import { combineReducers } from 'redux';

import * as actionsTypes from './actionsTypes';

const initialState = {
  battles: {},
  battlesId: [],
  pokemons: {},
  teams: {},
  users: {},
};

const battleReducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case actionsTypes.BATTLE_DETAIL:
      return {
        ...state,
        battles: {
          ...state.battles,
          ...action.payload.entities.battle,
        },
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
    case actionsTypes.POKEMON_LIST:
      return {
        pokemons: action.payload,
      };
    default:
      return state;
  }
};

export const rootReducer = combineReducers({
  battleR: battleReducer,
});
