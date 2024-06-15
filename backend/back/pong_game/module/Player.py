from .Paddle import Paddle
from .GameSetValue import PlayerStatus


class Player:
    """
    플레이어 클래스
    """

    def __init__(self, number: int, intra_id: str, nickname: str = None):
        self.__number: int = number
        self.__intra_id: str = intra_id
        self.__nickname: str = nickname if nickname else intra_id
        self.__status: PlayerStatus = PlayerStatus.WAIT
        self.__paddle: Paddle = Paddle(number)

    def get_number(self) -> int:
        return self.__number

    def get_intra_id(self) -> str:
        return self.__intra_id

    def get_nickname(self) -> str:
        return self.__nickname

    def get_status(self) -> PlayerStatus:
        return self.__status

    def get_paddle(self) -> Paddle:
        return self.__paddle

    def set_status(self, status: PlayerStatus) -> None:
        self.__status = status

    def set_number(self, number: int) -> None:
        self.__number = number
        self.__paddle.reset_position(number)

    def paddle_handler(self, key_input: str) -> None:
        self.__paddle.input_handler(key_input)
