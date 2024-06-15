from . import GameSetValue
from .GameSetValue import FIELD_WIDTH, BALL_SPEED_X, BALL_RADIUS, PADDLE_CORRECTION


class Ball:
    """
    Ball class
    """

    def __init__(self):
        self.__position_x: float = 0
        self.__position_z: float = 0
        self.__position_y: float = (
            -((self.__position_z - 1) * (self.__position_z - 1) / 5000) + 435
        )
        self.__radius: float = BALL_RADIUS
        self.__speed_x: float = BALL_SPEED_X
        # test 할때 속도를 받아오기 위해서 BALL_SPEED_Z를 GameSetValue.BALL_SPEED_Z로 수정
        self.__speed_z: float = GameSetValue.BALL_SPEED_Z
        self.__paddle_correction = PADDLE_CORRECTION

    def reset_position(self) -> None:
        """
        득점하거나 게임이 끝난 후 공의 위치를 초기화하는 함수
        """
        self.__position_x = 0
        self.__position_z = 0
        self.__position_y = (
            -((self.__position_z - 1) * (self.__position_z - 1) / 5000) + 435
        )
        self.__speed_x = BALL_SPEED_X
        self.__speed_z = GameSetValue.BALL_SPEED_Z
        self.__paddle_correction = PADDLE_CORRECTION

    def update_ball_position(self) -> None:
        """
        공의 속도에 따라 공의 위치를 업데이트하는 함수
        """
        self.__position_x += self.__speed_x
        self.__position_z += self.__speed_z
        self.__position_y = (
            -((self.__position_z - 1) * (self.__position_z - 1) / 5000) + 435
        )

    def is_side_collision(self) -> bool:
        """
        공이 좌우 벽에 부딪혔는지 확인하는 함수
        Returns:
            bool: 공이 좌우 벽에 부딪혔으면 True, 아니면 False
        """
        half_field_width = (FIELD_WIDTH - 2) / 2
        return (
            self.__position_x - self.__radius < -half_field_width
            or self.__position_x + self.__radius > half_field_width
        )

    def hit_ball_back(self, paddle_x: float) -> None:
        """
        공이 패들에 부딪혔을 때의 처리를 하는 함수
        Args:
            paddle_x: paddle의 x 좌표

        Returns:
            None
        """
        self.__speed_x = (self.__position_x - paddle_x) / 5
        self.__speed_z *= -1

    def protego_maxima(self) -> None:
        """
        protego_maxima spell을 사용했을 때의 처리를 하는 함수
        Returns:
            None
        """
        self.__speed_z += 4 if self.__speed_z > 0 else -4
        self.__paddle_correction += 4

    @property
    def position_x(self) -> float:
        """
        공의 x 좌표를 반환하는 함수
        Returns:
            float: 공의 x 좌표
        """
        return self.__position_x

    @property
    def position_z(self) -> float:
        """
        공의 z 좌표를 반환하는 함수
        Returns:
            float: 공의 z 좌표
        """
        return self.__position_z

    @property
    def radius(self) -> float:
        """
        공의 반지름을 반환하는 함수
        Returns:
            float: 공의 반지름
        """
        return self.__radius

    @property
    def paddle_correction(self) -> float:
        """
        패들의 보정값을 반환하는 함수
        Returns:
            float: 패들의 보정값
        """
        return self.__paddle_correction

    @property
    def speed_x(self) -> float:
        """
        공의 x 속도를 반환하는 함수
        Returns:
            float: 공의 x 속도
        """
        return self.__speed_x

    @property
    def speed_z(self) -> float:
        """
        공의 z 속도를 반환하는 함수
        Returns:
            float: 공의 z 속도
        """
        return self.__speed_z

    @speed_x.setter
    def speed_x(self, value):
        self.__speed_x = value

    def get_position(self) -> tuple[float, float, float]:
        """
        공의 위치를 반환하는 함수
        Returns:
            tuple: 공의 x, y, z 좌표
        """
        return self.__position_x, self.__position_y, self.__position_z

    def get_speed(self) -> tuple[float, float]:
        """
        공의 속도를 반환하는 함수
        Returns:
            tuple: 공의 x, z 속도
        """
        return self.__speed_x, self.__speed_z
