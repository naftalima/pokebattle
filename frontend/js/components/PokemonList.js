/* eslint-disable react/prop-types */
import React from 'react';
import { SortableElement } from 'react-sortable-hoc';

import PokemonCard from './PokemonCard';

const SortableItem = SortableElement(PokemonCard);

const PokemonList = ({ items }) => {
  return (
    <div className="SortableListContainer">
      {items.map((x, i) => {
        return <SortableItem key={x.id} index={i} todo={x} />;
      })}
    </div>
  );
};

export default PokemonList;
