/* eslint-disable react/prop-types */
import React from 'react';

const ToDoItem = ({ todo }) => {
  return (
    <div key={todo.id}>
      <p>{todo.content}</p>
    </div>
  );
};

export default ToDoItem;
