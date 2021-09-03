from rest_framework import serializers

from battles.models import Battle, Team
from battles.services.logic_team import create_guest_opponent
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class BattleSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    opponent = UserSerializer()

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner", "created_at")


class CreateBattleSerializer(serializers.ModelSerializer):
    opponent = serializers.CharField(style={"base_template": "textarea.html"})

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")
        extra_kwargs = {"winner": {"required": False}}

    def validate_opponent(self, attrs):
        opponent_email = attrs
        try:
            opponent = User.objects.get(email=opponent_email)
        except User.DoesNotExist:
            opponent = create_guest_opponent(opponent_email)
        return opponent

    def validate(self, attrs):
        creator_email = User.objects.get(email=attrs["creator"])
        opponent_email = User.objects.get(email=attrs["opponent"])
        challenge_yourself = opponent_email == creator_email
        if challenge_yourself:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")
        return attrs

    def create(self, validated_data):
        battle = Battle.objects.create(**validated_data)
        Team.objects.create(battle=battle, trainer=battle.creator)
        Team.objects.create(battle=battle, trainer=battle.opponent)
        return battle
