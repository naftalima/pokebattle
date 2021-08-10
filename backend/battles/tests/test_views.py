from common.utils.tests import TestCaseUtils


class CreateBattleViewTest(TestCaseUtils):
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