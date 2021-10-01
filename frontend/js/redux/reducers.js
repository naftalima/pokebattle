import { combineReducers } from 'redux';

import { BATTLE_DETAIL, BATTLE_LIST } from './actionsTypes';

const initialState = { battle: null, battles: null };

const battleReducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case BATTLE_DETAIL:
      return {
        ...state,
        battle: action.payload,
      };
    case BATTLE_LIST:
      return {
        ...state,
        battles: action.payload,
      };
    default:
      return state;
  }
};

export const rootReducer = combineReducers({
  battle: battleReducer,
});
