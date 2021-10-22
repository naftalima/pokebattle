/* eslint-disable react/prop-types */
import React from 'react';

const ToDoItem = ({ todo }) => {
  return (
    <div className="card">
      <div className="pokemon-name">
        <p>{todo.name}</p>
      </div>
      <div className="pokemon-img">
        <img alt="pokemon" src={todo.img_url} />
      </div>
      <div className="card-body">
        <div className="pokemon-status">
          <strong>ATK/{todo.attack}</strong>
        </div>
        <div className="pokemon-status">
          <strong>DEF/{todo.defense}</strong>
        </div>
        <div className="pokemon-status">
          <strong>HP/{todo.hp}</strong>
        </div>
      </div>
    </div>
  );
};

export default ToDoItem;
