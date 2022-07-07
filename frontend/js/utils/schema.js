import { schema } from 'normalizr';

const user = new schema.Entity('users');

const pokemon = new schema.Entity('pokemon');

const teamEntity = new schema.Entity('team', {
  trainer: user,
  pokemons: [pokemon],
});

const battleEntity = new schema.Entity('battle', {
  creator: user,
  opponent: user,
  teams: [teamEntity],
  winner: user,
});

const battlesEntity = [battleEntity];

export { battlesEntity, battleEntity, teamEntity };
