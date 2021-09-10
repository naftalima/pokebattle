from rest_framework import serializers

from battles.models import Battle, Team, TeamPokemon
from battles.services.api_integration import (
    check_pokemons_exists_in_pokeapi,
    get_or_create_pokemon,
    get_pokemon_info,
)
from battles.services.logic_team import create_guest_opponent
from battles.services.logic_team_pokemon import (
    check_pokemons_unique,
    check_position_unique,
    check_team_sum_valid,
)
from pokemons.models import Pokemon
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
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent")

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


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ("id", "poke_id", "name", "img_url", "attack", "defense", "hp")


class SelectTeamSerializer(serializers.ModelSerializer):
    pokemon_1 = serializers.CharField(write_only=True)
    pokemon_2 = serializers.CharField(write_only=True)
    pokemon_3 = serializers.CharField(write_only=True)

    position_1 = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    position_2 = serializers.IntegerField(min_value=1, max_value=3, write_only=True)
    position_3 = serializers.IntegerField(min_value=1, max_value=3, write_only=True)

    class Meta:
        model = Team
        fields = (
            "pokemon_1",
            "position_1",
            "pokemon_2",
            "position_2",
            "pokemon_3",
            "position_3",
        )

    def validate(self, attrs):
        positions = [attrs["position_1"], attrs["position_2"], attrs["position_3"]]
        pokemon_names = [attrs["pokemon_1"], attrs["pokemon_2"], attrs["pokemon_3"]]

        is_positions_unique = check_position_unique(positions)
        if not is_positions_unique:
            raise serializers.ValidationError(
                "ERROR: Has repeated positions. Please select unique positions."
            )

        is_pokemons_unique = check_pokemons_unique(pokemon_names)
        if not is_pokemons_unique:
            raise serializers.ValidationError(
                "ERROR: Has repeated pokemon. Please select unique pokemons."
            )

        is_pokemons_valid = check_pokemons_exists_in_pokeapi(pokemon_names)
        if not is_pokemons_valid:
            raise serializers.ValidationError(
                "ERROR: It's not a valid pokemon. Please select an pokemons."
            )

        pokemons_data = [get_pokemon_info(pokemon_name) for pokemon_name in pokemon_names]

        is_team_sum_valid = check_team_sum_valid(pokemons_data)
        if not is_team_sum_valid:
            raise serializers.ValidationError(
                "ERROR: Your pokemons sum more than 600 points. Please select other pokemons."
            )

        attrs["pokemon_1"] = get_or_create_pokemon(pokemons_data[0])
        attrs["pokemon_2"] = get_or_create_pokemon(pokemons_data[1])
        attrs["pokemon_3"] = get_or_create_pokemon(pokemons_data[2])

        return attrs

    def update(self, instance, validated_data):
        instance.pokemons.clear()

        pokemon_1 = validated_data.pop("pokemon_1")
        pokemon_2 = validated_data.pop("pokemon_2")
        pokemon_3 = validated_data.pop("pokemon_3")

        position_1 = validated_data.pop("position_1")
        position_2 = validated_data.pop("position_2")
        position_3 = validated_data.pop("position_3")

        TeamPokemon.objects.create(team=instance, pokemon=pokemon_1, order=position_1)
        TeamPokemon.objects.create(team=instance, pokemon=pokemon_2, order=position_2)
        TeamPokemon.objects.create(team=instance, pokemon=pokemon_3, order=position_3)

        return instance
