from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    필요한 유저 정보만 직렬화하는 클래스
    """

    class Meta:
        model: Users = Users
        fields: tuple = (
            "user_id",
            "intra_id",
            "nickname",
            "profile_image",
            "win_count",
            "lose_count",
            "status",
            "house",
        )


class UsersDetailSerializer(serializers.ModelSerializer):
    """
    모든 유저 정보를 직렬화 하는 클래스
    """

    class Meta:
        model: Users = Users
        fields: tuple = (
            "user_id",
            "nickname",
            "profile_image",
            "win_count",
            "lose_count",
            "status",
            "intra_id",
            "created_time",
            "updated_time",
            "house",
        )
