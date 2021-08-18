from django.urls import reverse

from model_bakery import baker

from battles.models import Battle, TeamPokemon
from common.utils.tests import TestCaseUtils


class CreateBattleViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make("users.User")

    def test_logged_in_uses_correct_template(self):
        response = self.auth_client.get("/battle/new/")

        # Check our user is logged in
        self.assertEqual(str(response.context["user"]), self.user.email)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, "battles/battle-opponent.html")

    def test_redirect_if_not_logged_in(self):
        self.auth_client.logout()
        response = self.auth_client.get("/battle/new/")
        self.assertRedirects(response, "/login/?next=/battle/new/")
        self.assertEqual(response.status_code, 302)

    def test_challenge_yourself(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.user.id,
        }

        self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertFalse(battle)

        self.assertRaisesMessage(ValueError, "ERROR: You can't challenge yourself.")

    def test_create_battle_valid_opponent(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        response = self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertTrue(battle)

        self.assertEqual(response.status_code, 302)

    def test_challenge_none(self):
        battle_data = {
            "creator": self.user.id,
        }

        self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertFalse(battle)

        self.assertRaisesMessage(ValueError, "ERROR: You can't challenge yourself.")


class SelectTeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.battle = baker.make("battles.Battle", creator=self.creator, opponent=self.opponent)
        self.team = baker.make("battles.Team", battle=self.battle, trainer=self.creator)

    def test_redirect_if_not_logged_in(self):
        self.auth_client.logout()
        response = self.auth_client.get(
            reverse("battle-team-pokemons", kwargs={"pk": self.team.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))

    def test_logged_in_uses_correct_template(self):
        response = self.auth_client.get(
            reverse("battle-team-pokemons", kwargs={"pk": self.team.id})
        )
        self.assertEqual(str(response.context["user"]), self.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "battles/battle-team-pokemons.html")

    def test_creator_select_valid_team(self):
        team_pokemon_data = {
            "pokemon_1": "pikachu",
            "position_1": 1,
            "pokemon_2": "eevee",
            "position_2": 2,
            "pokemon_3": "nidorina",
            "position_3": 3,
        }
        response = self.auth_client.post(
            reverse(
                "battle-team-pokemons",
                kwargs={
                    "pk": self.team.id,
                },
            ),
            team_pokemon_data,
            follow=True,
        )
        team_pokemon = TeamPokemon.objects.filter(team=self.team)
        self.assertTrue(team_pokemon)

        self.assertRedirects(response, "/battle/")

    def test_creator_select_invalid_pokemon(self):
        team_pokemon_data = {
            "pokemon_1": "momo",
            "position_1": 1,
            "pokemon_2": "eevee",
            "position_2": 2,
            "pokemon_3": "nidorina",
            "position_3": 3,
        }
        self.auth_client.post(
            reverse(
                "battle-team-pokemons",
                kwargs={
                    "pk": self.team.id,
                },
            ),
            team_pokemon_data,
            follow=True,
        )

        team_pokemon = TeamPokemon.objects.filter(team=self.team)
        self.assertFalse(team_pokemon)
        self.assertRaisesMessage(ValueError, "ERROR: It's not a valid pokemon.")

    def test_missing_pokemon(self):
        team_pokemon_data = {
            "pokemon_1": "",
            "position_1": 1,
            "pokemon_2": "eevee",
            "position_2": 2,
            "pokemon_3": "nidorina",
            "position_3": 3,
        }
        self.auth_client.post(
            reverse(
                "battle-team-pokemons",
                kwargs={
                    "pk": self.team.id,
                },
            ),
            team_pokemon_data,
            follow=True,
        )

        team_pokemon = TeamPokemon.objects.filter(team=self.team)
        self.assertFalse(team_pokemon)
        self.assertRaisesMessage(ValueError, "ERROR: All fields are required.")
