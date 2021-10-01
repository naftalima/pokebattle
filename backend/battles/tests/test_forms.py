from model_bakery import baker

from battles.forms import TeamForm
from common.utils.tests import TestCaseUtils


class TeamFormTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team = baker.make("battles.Team", battle=self.battle, trainer=self.creator)

    def test_valid_form(self):
        """Happy Path"""
        team_data = {
            "pokemon_1": "pikachu",
            "position_1": "1",
            "pokemon_2": "eevee",
            "position_2": "2",
            "pokemon_3": "nidorina",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertTrue(form.is_valid())

    def test_missing_pokemon(self):
        team_data = {
            "pokemon_1": "",
            "position_1": "1",
            "pokemon_2": "eevee",
            "position_2": "2",
            "pokemon_3": "nidorina",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())

    def test_missing_position(self):
        team_data = {
            "pokemon_1": "charizard",
            "position_1": "",
            "pokemon_2": "eevee",
            "position_2": "2",
            "pokemon_3": "nidorina",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())

    def test_repeated_position(self):
        team_data = {
            "pokemon_1": "charmander",
            "position_1": "1",
            "pokemon_2": "eevee",
            "position_2": "1",
            "pokemon_3": "nidorina",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())

    def test_repeated_pokemon(self):
        team_data = {
            "pokemon_1": "charmander",
            "position_1": "1",
            "pokemon_2": "charmander",
            "position_2": "2",
            "pokemon_3": "charmander",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())

    def test_invalid_pokemon_name(self):
        team_data = {
            "pokemon_1": "appa",
            "position_1": "1",
            "pokemon_2": "momo",
            "position_2": "2",
            "pokemon_3": "pikachu",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())

    def test_invalid_team_sum(self):
        team_data = {
            "pokemon_1": "bulbasaur",
            "position_1": "1",
            "pokemon_2": "ivysaur",
            "position_2": "1",
            "pokemon_3": "venusaur",
            "position_3": "3",
        }
        form = TeamForm(data=team_data)

        self.assertFalse(form.is_valid())
