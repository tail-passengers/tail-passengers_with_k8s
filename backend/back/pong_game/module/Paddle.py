from .GameSetValue import (
    PADDLE_SPEED,
    FIELD_LENGTH,
    KeyboardInput,
    PADDLE_BOUNDARY,
)


class Paddle:
    def __init__(self, number: int):
        self.__number: int = number
        self.__position_x: float = 0
        self.__position_y: float = 0
        self.__position_z: float = (
            FIELD_LENGTH / 2 if self.__number == 1 else -FIELD_LENGTH / 2
        )
        self.__left: bool = False
        self.__right: bool = False

    def input_handler(self, key_input: str) -> None:
        """
        키보드 입력에 따라 패들을 움직이는 함수
        Args:
            key_input: 받은 키보드 입력

        Returns:
            None
        """
        if key_input == KeyboardInput.LEFT_PRESS.value:
            self.__left = True
        elif key_input == KeyboardInput.LEFT_RELEASE.value:
            self.__left = False
        elif key_input == KeyboardInput.RIGHT_PRESS.value:
            self.__right = True
        elif key_input == KeyboardInput.RIGHT_RELEASE.value:
            self.__right = False

    def move_handler(self, player_num: int) -> None:
        """
        플레이어가 누른 키에 따라 패들을 움직이는 함수
        Args:
            player_num: 플레이어의 번호

        Returns:
            None
        """
        if player_num == 1:
            if self.__left and not self.__right:
                self.__move(-1)
            elif not self.__left and self.__right:
                self.__move(1)
        elif player_num == 2:
            if self.__left and not self.__right:
                self.__move(1)
            elif not self.__left and self.__right:
                self.__move(-1)

    def reset_position(self, number: int) -> None:
        """
        패들의 위치를 초기화하는 함수
        Args:
            number: 플레이어의 번호

        Returns:
            None
        """
        self.__number = number
        self.__position_x = 0
        self.__position_y = 0
        self.__position_z = (
            FIELD_LENGTH / 2 if self.__number == 1 else -FIELD_LENGTH / 2
        )
        self.__left = False
        self.__right = False

    def __move(self, direction: int) -> None:
        """
        패들을 움직이는 함수
        Args:
            direction: 움직이는 방향

        Returns:
            None
        """
        new_paddle_x = self.__position_x + direction * PADDLE_SPEED
        self.__position_x = max(
            -PADDLE_BOUNDARY,
            min(PADDLE_BOUNDARY, new_paddle_x),
        )

    @property
    def position_x(self) -> float:
        """
        position_x를 반환하는 함수
        Returns:
            float: position_x
        """
        return self.__position_x

    @property
    def position_z(self) -> float:
        """
        position_z를 반환하는 함수
        Returns:
            float: position_z
        """
        return self.__position_z
