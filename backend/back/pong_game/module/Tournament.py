import json
from typing import Optional
from .GameSetValue import (
    TournamentStatus,
    MessageType,
    PlayerNumber,
    TOURNAMENT_PLAYER_MAX_CNT,
    PlayerStatus,
    TournamentGroupName,
    RoundNumber,
    GameStatus,
    GameTimeType,
)
from .Player import Player
from .Round import Round


class Tournament:
    """
    토너먼트 클래스
    """

    def __init__(
        self,
        tournament_name: str,
        create_user_intra_id: str,
        create_user_nickname: str,
    ):
        self.__tournament_name: str = tournament_name
        self.__round_list: list[Optional[Round]] = [None, None, None]
        self.__player_list: list[Optional[Player]] = [
            Player(
                number=1, intra_id=create_user_intra_id, nickname=create_user_nickname
            ),
            None,
            None,
            None,
        ]
        self.__nickname_list: list[str] = ["", "", "", ""]
        self.__player_total_cnt: int = 1
        self.__status: TournamentStatus = TournamentStatus.WAIT

    def build_tournament_wait_dict(self) -> dict:
        """
        대기 중인 토너먼트 정보를 딕셔너리 형태로 반환하는 함수
        Returns:
            dict: 대기 중인 토너먼트 정보
        """
        return {
            "tournament_name": self.__tournament_name,
            "wait_num": str(self.__player_total_cnt),
        }

    def _join_tournament_with_intra_id(
        self, intra_id: str, nickname: str
    ) -> PlayerNumber:
        """
        토너먼트에 참가하는 함수
        Args:
            intra_id: 참가자의 intra_id
            nickname: 참가자의 닉네임

        Returns:
            PlayerNumber: 참가자의 번호
        """
        for idx, player in enumerate(self.__player_list):
            if player is None:
                self.__player_list[idx] = Player(
                    number=2 if idx % 2 else 1, intra_id=intra_id, nickname=nickname
                )
                self.__player_total_cnt += 1
                if self.__player_total_cnt == TOURNAMENT_PLAYER_MAX_CNT:
                    self.__status = TournamentStatus.READY
                return list(PlayerNumber)[idx]
            elif player.get_intra_id() == intra_id:
                return PlayerNumber.PLAYER_1

    def build_tournament_wait_detail_json(
        self, intra_id: str, nickname: str
    ) -> tuple[str, json]:
        """
        대기 중인 토너먼트 정보를 json 형태로 반환하는 함수
        Args:
            intra_id: 참가자의 intra_id
            nickname: 참가자의 닉네임

        Returns:
            str: 참가자의 번호
            json: 대기 중인 토너먼트 정보
        """
        player_number = self._join_tournament_with_intra_id(
            intra_id=intra_id, nickname=nickname
        ).value
        return player_number, json.dumps(
            {
                "message_type": MessageType.WAIT.value,
                "nickname": nickname,
                "total": self.__player_total_cnt,
                "number": player_number,
            }
        )

    def build_tournament_ready_json(
        self,
        team_name: TournamentGroupName,
        player1_nickname: str = None,
        player2_nickname: str = None,
    ) -> json:
        """
        토너먼트 시작을 알리는 json을 반환하는 함수
        Args:
            team_name: 현재 라운드의 팀 이름
            player1_nickname: 플레이어1의 닉네임
            player2_nickname: 플레이어2의 닉네임

        Returns:
            json: 토너먼트 시작을 알리는 json
        """
        if team_name == TournamentGroupName.A_TEAM:
            self.__round_list[0] = Round(
                self.__player_list[0], self.__player_list[1], RoundNumber.ROUND_1
            )
            return json.dumps(
                {
                    "message_type": MessageType.READY.value,
                    "round": RoundNumber.ROUND_1.value,
                    "1p": self.__player_list[0].get_nickname(),
                    "2p": self.__player_list[1].get_nickname(),
                }
            )
        elif team_name == TournamentGroupName.B_TEAM:
            self.__round_list[1] = Round(
                self.__player_list[2], self.__player_list[3], RoundNumber.ROUND_2
            )
            return json.dumps(
                {
                    "message_type": MessageType.READY.value,
                    "round": RoundNumber.ROUND_2.value,
                    "1p": self.__player_list[2].get_nickname(),
                    "2p": self.__player_list[3].get_nickname(),
                }
            )
        elif team_name == TournamentGroupName.FINAL_TEAM:
            player1, player2 = None, None
            for idx, player in enumerate(self.__player_list):
                if player.get_nickname() == player1_nickname:
                    player1 = player
                elif player.get_nickname() == player2_nickname:
                    player2 = player
            player1.set_status(PlayerStatus.READY)
            player2.set_status(PlayerStatus.READY)
            player1.set_number(1)
            player2.set_number(2)
            self.__round_list[2] = Round(player1, player2, RoundNumber.ROUND_3)
            return json.dumps(
                {
                    "message_type": MessageType.READY.value,
                    "round": RoundNumber.ROUND_3.value,
                    "1p": player1_nickname,
                    "2p": player2_nickname,
                }
            )

    def build_tournament_complete_json(self, is_error=False) -> json:
        """
        토너먼트 종료를 알리는 json을 반환하는 함수
        Args:
            is_error: 에러가 발생했는지 여부

        Returns:
            json: 토너먼트 종료를 알리는 json
        """
        return json.dumps(
            {
                "message_type": (
                    MessageType.ERROR.value if is_error else MessageType.COMPLETE.value
                ),
                "winner": self.__round_list[2].get_winner(),
                "loser": self.__round_list[2].get_loser(),
                "etc1": self.__round_list[0].get_loser(),
                "etc2": self.__round_list[1].get_loser(),
            }
        )

    def disconnect_tournament(self, nickname: str) -> json:
        """
        토너먼트 참가자가 나갔을 때의 처리를 하는 함수
        Args:
            nickname: 나간 참가자의 닉네임

        Returns:
            json: 나간 참가자의 정보
        """
        data = {"message_type": MessageType.WAIT.value}
        for idx, player in enumerate(self.__player_list):
            if player is not None and player.get_nickname() == nickname:
                self.__player_list[idx] = None
                self.__player_total_cnt -= 1
                data["nickname"] = nickname
                data["total"] = self.__player_total_cnt
                data["number"] = list(PlayerNumber)[idx].value
        return json.dumps(data)

    def is_all_ready(self) -> bool:
        """
        모든 참가자가 레디 상태인지 확인하는 함수
        Returns:
            bool: 모든 참가자가 레디 상태이면 True, 아니면 False
        """
        for player in self.__player_list:
            if player is None:
                return False
            if player.get_status() != PlayerStatus.READY:
                return False
        self.__nickname_list = [player.get_nickname() for player in self.__player_list]
        return True

    def is_all_round_ready(self):
        """
        모든 라운드가 레디 상태인지 확인하는 함수
        Returns:
            bool: 모든 라운드가 레디 상태이면 True, 아니면 False
        """
        if self.__round_list[0].is_all_ready() and self.__round_list[1].is_all_ready():
            return True
        return False

    def get_status(self) -> TournamentStatus:
        return self.__status

    def get_player_total_cnt(self) -> int:
        return self.__player_total_cnt

    def get_round(self, round_number: int) -> Round:
        return self.__round_list[round_number - 1]

    def get_db_datas(self, round_number: int) -> dict:
        """
        라운드에 대한 db 데이터를 반환하는 함수
        Args:
            round_number: round number

        Returns:
            dict: 라운드에 대한 db 데이터
        """
        db_data = self.__round_list[round_number - 1].get_db_data()
        db_data["tournament_name"] = self.__tournament_name
        db_data["round"] = round_number
        db_data["is_final"] = round_number == 3
        return db_data

    def get_winner_loser_intra_ids(self, round_number: int) -> tuple:
        return self.__round_list[round_number - 1].get_winner_loser_intra_id()

    @property
    def tournament_name(self) -> str:
        return self.__tournament_name

    @property
    def player_list(self) -> list[Optional[Player]]:
        return self.__player_list

    def set_status(self, status: TournamentStatus) -> None:
        self.__status = status

    def try_set_ready(self, player_number: str, nickname: str) -> bool:
        """
        플레이어의 레디 상태를 설정하는 함수
        Args:
            player_number: 플레이어의 번호
            nickname: 플레이어의 닉네임

        Returns:
            bool: 레디 상태가 설정되면 True, 아니면 False
        """
        player_numbers = [player.value for player in PlayerNumber]
        idx = player_numbers.index(player_number)
        if (
            self.__player_list[idx] is None
            or self.__player_list[idx].get_nickname() != nickname
        ):
            return False
        self.__player_list[idx].set_status(PlayerStatus.READY)
        return True

    def set_round_status(self, status: GameStatus, is_final: bool) -> None:
        if is_final:
            self.__round_list[int(RoundNumber.FINAL_NUMBER.value) - 1].set_status(
                status
            )
        else:
            for i in range(int(RoundNumber.FINAL_NUMBER.value) - 1):
                self.__round_list[i].set_status(status)

    def set_round_game_time(self, time_type: GameTimeType, is_final: bool) -> None:
        if is_final:
            self.__round_list[int(RoundNumber.FINAL_NUMBER.value) - 1].set_game_time(
                time_type=time_type.value
            )
        else:
            for i in range(int(RoundNumber.FINAL_NUMBER.value) - 1):
                self.__round_list[i].set_game_time(time_type=time_type.value)
