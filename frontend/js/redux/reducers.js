import { combineReducers } from 'redux';

import { BATTLE_DETAIL } from './actions';

const initialState = { battle: null };

const battleReducer = (state = initialState, action = {}) => {
  if (action.type === BATTLE_DETAIL) {
    return {
      ...state,
      battle: action.payload,
    };
  }
  return state;
};

export const rootReducer = combineReducers({
  battle: battleReducer,
});
