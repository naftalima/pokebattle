/* eslint-disable react/prop-types */
import React from 'react';
import { SortableElement } from 'react-sortable-hoc';

import ToDoItem from './ToDoItem';

const SortableItem = SortableElement(ToDoItem);

const ToDoList = ({ items }) => {
  return (
    <div>
      {items.map((x, i) => {
        return <SortableItem key={x.id} index={i} todo={x} />;
      })}
    </div>
  );
};

export default ToDoList;
