from django.urls import reverse

from model_bakery import baker

from battles.models import Battle
from common.utils.tests import TestCaseUtils


class BattleListTests(TestCaseUtils):
    view_name = "api:battle_list"

    def setUp(self):
        super().setUp()
        self.view_url = reverse(self.view_name)

    def test_return_200_when_accessing_endpoint(self):
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)

    def test_return_queryset(self):
        battle = baker.make("battles.Battle", creator=self.user)
        response = self.auth_client.get(self.view_url)
        self.assertTrue(response.data)

        self.assertEqual(response.data[0].get("id"), battle.id)

    def test_return_empty_queryset(self):
        baker.make("battles.Battle")
        response = self.auth_client.get(self.view_url)
        self.assertFalse(response.data)


class CreateBattleTest(TestCaseUtils):
    view_name = "api:battle_create"

    def setUp(self):
        super().setUp()
        self.creator = self.user
        self.opponent = baker.make("users.User")
        self.view_url = reverse(self.view_name)

    def test_create_battle_valid_opponent(self):
        battle_data = {
            "opponent": self.opponent.email,
        }

        response = self.auth_client.post(self.view_url, battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertEqual(battle[0].creator.email, self.user.email)
        self.assertEqual(battle[0].opponent.email, self.opponent.email)

        self.assertTrue(battle)

        self.assertEqual(response.status_code, 201)

    def test_challenge_none(self):
        battle_data = {}

        self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertFalse(battle)

    def test_challenge_yourself(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.user.id,
        }

        self.auth_client.post(reverse("battle-opponent"), battle_data)

        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertFalse(battle)

        self.assertRaisesMessage(ValueError, "ERROR: You can't challenge yourself.")
