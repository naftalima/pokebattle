import { schema } from 'normalizr';

const user = new schema.Entity('users');

const pokemon = new schema.Entity('pokemon');

const team = new schema.Entity('team', {
  trainer: user,
  pokemons: [pokemon],
});

const battleEntity = new schema.Entity('battle', {
  creator: user,
  opponent: user,
  teams: [team],
  winner: user,
});

const battlesEntity = [battleEntity];

export { battlesEntity, battleEntity };
