from django.urls import reverse

from model_bakery import baker

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
        """ """
        baker.make("battles.Battle")
        response = self.auth_client.get(self.view_url)
        self.assertFalse(response.data)
