from django.urls import reverse

from model_bakery import baker

from battles.models import Battle
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
