import json

from .GeneralGame import GeneralGame
from .GameSetValue import RoundNumber, PlayerStatus, MessageType
from .Player import Player


class Round(GeneralGame):
    """
    라운드 클래스
    """

    def __init__(self, player1: Player, player2: Player, round_number: RoundNumber):
        super().__init__(player1, player2)
        self.__round_number: RoundNumber = round_number
        self.__winner: str = ""
        self.__loser: str = ""
        self.__is_closed: bool = False

    def build_start_json(self) -> json:
        """
        라운드 시작 메시지를 json 형태로 반환하는 함수
        Returns:
            json: 라운드 시작 메시지
        """
        return json.dumps(
            {
                "message_type": MessageType.START.value,
                "round": self.__round_number.value,
            }
        )

    def build_end_json(self) -> json:
        """
        라운드 종료 메시지를 json 형태로 반환하는 함수
        Returns:
            json: 라운드 종료 메시지
        """
        self.__winner = (
            self._player1.get_nickname()
            if self._score1 > self._score2
            else self._player2.get_nickname()
        )
        self.__loser = (
            self._player2.get_nickname()
            if self._score1 > self._score2
            else self._player1.get_nickname()
        )
        return json.dumps(
            {
                "message_type": MessageType.END.value,
                "round": self.__round_number.value,
                "winner": self.__winner,
                "loser": self.__loser,
            }
        )

    def build_stay_json(self) -> json:
        """
        라운드 종료 메시지를 json 형태로 반환하는 함수
        Returns:
            json: 라운드 종료 메시지
        """
        self.__winner = (
            self._player1.get_nickname()
            if self._score1 > self._score2
            else self._player2.get_nickname()
        )
        self.__loser = (
            self._player2.get_nickname()
            if self._score1 > self._score2
            else self._player1.get_nickname()
        )
        return json.dumps(
            {
                "message_type": MessageType.STAY.value,
                "round": self.__round_number.value,
                "winner": self.__winner,
                "loser": self.__loser,
            }
        )

    def is_all_ready(self) -> bool:
        """
        두 플레이어가 모두 라운드 준비가 되었는지 확인하는 함수
        Returns:
            bool: 두 플레이어가 모두 라운드 준비가 되었으면 True, 아니면 False
        """
        if self._player1 is None or self._player2 is None:
            return False
        if (
            self._player1.get_status()
            == self._player2.get_status()
            == PlayerStatus.ROUND_READY
        ):
            return True
        return False

    def get_winner(self) -> str:
        return self.__winner

    def get_loser(self) -> str:
        return self.__loser

    def get_nicknames(self) -> tuple[str, str]:
        return self._player1.get_nickname(), self._player2.get_nickname()

    def get_is_closed(self) -> bool:
        return self.__is_closed

    def set_round_ready(self, intra_id: str) -> None:
        if intra_id == self._player1.get_intra_id():
            self._player1.set_status(PlayerStatus.ROUND_READY)
        elif intra_id == self._player2.get_intra_id():
            self._player2.set_status(PlayerStatus.ROUND_READY)

    def set_is_closed(self, is_closed: bool) -> None:
        self.__is_closed = is_closed
