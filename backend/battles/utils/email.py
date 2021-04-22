from templated_email import send_templated_mail


def email_test(winner, creator, creator_pkms, opponent, opponent_pkms):
    send_templated_mail(
        template_name="battle_result",
        from_email="nathalia.lima@vinta.com.br",
        recipient_list=[creator.email, opponent.email],
        context={
            "winner": winner,
            "creator": creator,
            "creator_pkms": creator_pkms,
            "opponent_pkms": opponent_pkms,
            "opponent": opponent,
        },
    )
