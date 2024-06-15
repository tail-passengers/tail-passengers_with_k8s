import uuid
from datetime import datetime
from typing import Optional, Union
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self, intra_id: str, nickname: Optional[str] = None, **extra_fields
    ):
        """
        주어진 intra id와 nickname으로 새로운 유저를 생성하는 함수
        Args:
            intra_id: 유저의 intra ID
            nickname: 유저의 닉네임(기본값은 intra_id)
            **extra_fields: 추가 필드

        Returns:
            Users: 생성된 유저 객체
        """
        if not intra_id:
            raise ValueError("The Intra ID must be set")
        user: Users = self.model(
            intra_id=intra_id,
            nickname=nickname if nickname else intra_id,
            **extra_fields
        )
        user.save(using=self._db)
        user.set_unusable_password()
        return user

    def create_superuser(self, intra_id: str, **extra_fields):
        """
        주어진 intra id로 superuser를 생성하는 함수
        Args:
            intra_id: 유저의 intra ID
            **extra_fields: 추가 필드

        Returns:
            Users: 생성된 superuser 객체
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(intra_id, **extra_fields)


class UserStatusEnum(models.TextChoices):
    """
    유저의 접속 상태를 나타내는 Enum 클래스
    """

    ONLINE = "1", "Online"
    OFFLINE = "0", "Offline"


class HouseEnum(models.TextChoices):
    """
    유저의 소속 집단을 나타내는 Enum 클래스
    """

    GRYFFINDOR = "GR"
    RAVENCLAW = "RA"
    SLYTHERIN = "SL"
    HUFFLEPUFF = "HU"


class Users(AbstractBaseUser, PermissionsMixin):
    """
    유저 정보를 저장하는 모델 클래스
    """

    user_id: Union[str, uuid.UUID] = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    intra_id: str = models.CharField(max_length=20, unique=True, editable=False)
    nickname: str = models.CharField(max_length=20, unique=True)
    profile_image: str = models.ImageField(
        null=True, blank=True, upload_to="profile_images"
    )
    house: str = models.CharField(choices=HouseEnum.choices, max_length=2)
    win_count: int = models.IntegerField(default=0)
    lose_count: int = models.IntegerField(default=0)
    created_time: datetime = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time: datetime = models.DateTimeField(auto_now=True)
    status: str = models.CharField(
        max_length=2, choices=UserStatusEnum.choices, default=UserStatusEnum.OFFLINE
    )
    is_test_user: bool = models.BooleanField(default=False)

    is_staff: bool = models.BooleanField(
        default=False
    )  # 추가: 관리자 사이트에 로그인하기 위해 필요
    is_active: bool = models.BooleanField(default=True)  # 추가: 사용자가 활성 상태인지
    session_key = models.CharField(max_length=40, null=True, blank=True)

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = "intra_id"
    REQUIRED_FIELDS: list[str] = ["nickname"]

    class Meta:
        db_table: str = "Users"
        ordering: list[str] = ["created_time"]

    def __str__(self) -> str:
        return self.intra_id
