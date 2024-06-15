import json
from datetime import datetime
from typing import Optional
from .Player import Player
from .Ball import Ball
from .GameSetValue import (
    PlayerStatus,
    PADDLE_WIDTH,
    MessageType,
    GameTimeType,
    MAX_SCORE,
    GameStatus,
)


class GeneralGame:
    """
    GeneralGame class
    """

    def __init__(self, player1: Player, player2: Player):
        self.__ball: Ball = Ball()
        self._player1: Player = player1
        self._player2: Player = player2
        self._score1: int = 0
        self._score2: int = 0
        self.__status: GameStatus = GameStatus.WAIT
        self.__start_time: Optional[datetime] = None
        self.__end_time: Optional[datetime] = None

    def is_all_ready(self) -> bool:
        """
        모든 플레이어가 준비가 되었는지 확인하는 함수
        Returns:
            bool: 모든 플레이어가 준비가 되었으면 True, 아니면 False
        """
        if self._player1 is None or self._player2 is None:
            return False
        if (
            self._player1.get_status()
            == self._player2.get_status()
            == PlayerStatus.READY
        ):
            return True
        return False

    def __is_past_paddle1(self) -> bool:
        """
        공이 플레이어1의 패들을 지나쳤는지 확인하는 함수
        Returns:
            bool: 공이 플레이어1의 패들을 지나쳤으면 True, 아니면 False
        """
        return (
            self.__ball.position_z
            > self._player1.get_paddle().position_z + self.__ball.paddle_correction
        )

    def __is_past_paddle2(self) -> bool:
        """
        공이 플레이어2의 패들을 지나쳤는지 확인하는 함수
        Returns:
            bool: 공이 플레이어2의 패들을 지나쳤으면 True, 아니면 False
        """
        return (
            self.__ball.position_z
            < self._player2.get_paddle().position_z - self.__ball.paddle_correction
        )

    def __is_paddle1_collision(self) -> bool:
        """
        공이 플레이어1의 패들과 충돌했는지 확인하는 함수
        Returns:
            bool: 공이 플레이어1의 패들과 충돌했으면 True, 아니면 False
        """
        return (
            self.__ball.position_z + self.__ball.radius
            >= self._player1.get_paddle().position_z
            and self.__is_ball_aligned_with_paddle(1)
        )

    def __is_paddle2_collision(self) -> bool:
        """
        공이 플레이어2의 패들과 충돌했는지 확인하는 함수
        Returns:
            bool: 공이 플레이어2의 패들과 충돌했으면 True, 아니면 False
        """
        return (
            self.__ball.position_z - self.__ball.radius
            <= self._player2.get_paddle().position_z
            and self.__is_ball_aligned_with_paddle(2)
        )

    def __is_ball_aligned_with_paddle(self, paddle_num: int) -> bool:
        """
        공이 패들과 정렬되어 있는지 확인하는 함수
        Args:
            paddle_num: 패들 번호

        Returns:
            bool: 공이 패들과 정렬되어 있으면 True, 아니면 False
        """
        half_paddle_width = PADDLE_WIDTH / 2
        paddle = (
            self._player1.get_paddle()
            if paddle_num == 1
            else self._player2.get_paddle()
        )
        return (
            paddle.position_x - half_paddle_width
            < self.__ball.position_x
            < paddle.position_x + half_paddle_width
        )

    def __reset_position(self) -> None:
        """
        공의 위치를 초기화하는 함수
        Returns:
            None
        """
        self.__ball.reset_position()

    def key_input(self, text_data: json) -> None:
        data = json.loads(text_data)
        if data["input"] == "protego_maxima":
            self.__ball.protego_maxima()
        elif data["number"] == "player1":
            self._player1.paddle_handler(data["input"])
        elif data["number"] == "player2":
            self._player2.paddle_handler(data["input"])

    @staticmethod
    def build_ready_json(number: int, nickname: str) -> json:
        """
        ready json을 만드는 함수
        Args:
            number: player 위치
            nickname: player 닉네임

        Returns:
            json: ready json
        """
        return json.dumps(
            {
                "message_type": MessageType.READY.value,
                "number": "player1" if number == 1 else "player2",
                "nickname": nickname,
            }
        )

    def build_start_json(self) -> json:
        """
        start json을 만드는 함수
        Returns:
            json: start json
        """
        return json.dumps(
            {
                "message_type": MessageType.START.value,
                "1p": self._player1.get_nickname(),
                "2p": self._player2.get_nickname(),
            }
        )

    def build_game_json(self, game_start: bool = True) -> json:
        """
        game json을 만드는 함수
        Args:
            game_start: game이 이제 시작해서 공을 멈춰야 하는지 여부

        Returns:
            json: game json
        """
        self.__move_paddle()
        if game_start:
            self.__move_ball()
        paddle1 = self._player1.get_paddle().position_x
        paddle2 = self._player2.get_paddle().position_x
        ball_x, ball_y, ball_z = self.__ball.get_position()
        ball_vx, ball_vz = self.__ball.get_speed()
        return json.dumps(
            {
                "message_type": MessageType.PLAYING.value,
                "paddle1": paddle1,
                "paddle2": paddle2,
                "ball_x": ball_x,
                "ball_y": ball_y,
                "ball_z": ball_z,
                "ball_vx": ball_vx,
                "ball_vz": ball_vz,
            }
        )

    def build_score_json(self) -> json:
        """
        score json을 만드는 함수
        Returns:
            json: score json
        """
        return json.dumps(
            {
                "message_type": MessageType.SCORE.value,
                "player1_score": self._score1,
                "player2_score": self._score2,
            }
        )

    def build_end_json(self) -> json:
        """
        end json을 만드는 함수
        Returns:
            json: end json
        """
        return json.dumps(
            {
                "message_type": MessageType.END.value,
                "winner": "player1" if self._score1 > self._score2 else "player2",
                "loser": "player2" if self._score1 > self._score2 else "player1",
            }
        )

    def build_error_json(self, nickname: str) -> json:
        """
        error json을 만드는 함수
        Args:
            nickname: player 닉네임

        Returns:
            json: error json
        """
        self.__status = GameStatus.END
        return json.dumps(
            {
                "message_type": MessageType.ERROR.value,
                "nickname": nickname,
            }
        )

    def build_complete_json(self, is_error=False) -> json:
        """
        complete json을 만드는 함수
        Args:
            is_error: db에 저장할 때 error인지 확인하는 변수

        Returns:
            json: complete json
        """
        return json.dumps(
            {
                "message_type": (
                    MessageType.ERROR.value if is_error else MessageType.COMPLETE.value
                ),
                "winner": (
                    self._player1.get_nickname()
                    if self._score1 > self._score2
                    else self._player2.get_nickname()
                ),
                "loser": (
                    self._player2.get_nickname()
                    if self._score1 > self._score2
                    else self._player1.get_nickname()
                ),
            }
        )

    def __move_paddle(self) -> None:
        """
        패들을 움직이는 함수
        Returns:
            None
        """
        self._player1.get_paddle().move_handler(player_num=1)
        self._player2.get_paddle().move_handler(player_num=2)

    def __move_ball(self) -> None:
        """
        공을 움직이는 함수
        Returns:
            None
        """
        self.__ball.update_ball_position()
        if self.__is_past_paddle1():
            self._score2 += 1
            self.__reset_position()
            self.__status = GameStatus.SCORE
        elif self.__is_past_paddle2():
            self._score1 += 1
            self.__reset_position()
            self.__status = GameStatus.SCORE
        elif self.__ball.is_side_collision():
            self.__ball.speed_x = self.__ball.speed_x * -1
        elif self.__is_paddle1_collision():
            self.__ball.hit_ball_back(self._player1.get_paddle().position_x)
        elif self.__is_paddle2_collision():
            self.__ball.hit_ball_back(self._player2.get_paddle().position_x)

    def get_player(self, intra_id: str) -> Optional[tuple[Player, int]]:
        """
        플레이어를 반환하는 함수
        Args:
            intra_id: 찾을 플레이어의 intra_id

        Returns:
            Optional[tuple[Player, int]]: 플레이어와 플레이어 번호
        """
        if self._player1.get_intra_id() == intra_id:
            return self._player1, 1
        elif self._player2.get_intra_id() == intra_id:
            return self._player2, 2
        return None

    def get_status(self) -> GameStatus:
        """
        게임의 상태를 반환하는 함수
        Returns:
            GameStatus: 게임의 상태
        """
        return self.__status

    def get_score(self) -> tuple[int, int]:
        """
        게임의 점수를 반환하는 함수
        Returns:
            tuple: 플레이어1의 점수, 플레이어2의 점수
        """
        return self._score1, self._score2

    def get_ball_position(self) -> tuple[float, float]:
        """
        공의 위치를 반환하는 함수
        Returns:
            tuple: 공의 x 좌표, 공의 z 좌표
        """
        return self.__ball.position_x, self.__ball.position_z

    def get_ball_speed(self) -> tuple[float, float]:
        """
        공의 속도를 반환하는 함수
        Returns:
            tuple: 공의 x 속도, 공의 z 속도
        """
        return self.__ball.speed_x, self.__ball.speed_z

    def get_game_time(self, time_type: GameTimeType) -> datetime:
        """
        게임의 시간을 반환하는 함수
        Args:
            time_type: 시작 시간인지 끝 시간인지 확인하는 변수

        Returns:
            datetime: 게임의 시간
        """
        if time_type == GameTimeType.START_TIME.value:
            return self.__start_time
        elif time_type == GameTimeType.END_TIME.value:
            return self.__end_time

    def set_game_time(self, time_type: GameTimeType) -> None:
        """
        게임의 시간을 설정하는 함수
        Args:
            time_type: 시작 시간인지 끝 시간인지 확인하는 변수

        Returns:
            None
        """
        if time_type == GameTimeType.START_TIME.value:
            self.__start_time = datetime.now()
        elif time_type == GameTimeType.END_TIME.value:
            self.__end_time = datetime.now()

    def get_db_data(self) -> dict:
        """
        db에 저장할 데이터를 반환하는 함수
        Returns:
            dict: db에 저장할 데이터
        """
        return {
            "start_time": self.__start_time,
            "end_time": self.__end_time,
            "player1_intra_id": self._player1.get_intra_id(),
            "player2_intra_id": self._player2.get_intra_id(),
            "player1_score": self._score1,
            "player2_score": self._score2,
        }

    def get_winner_loser_intra_id(self) -> tuple[Optional[str], Optional[str]]:
        """
        승자와 패자의 intra_id를 반환하는 함수
        Returns:
            tuple: 승자의 intra_id, 패자의 intra_id
        """
        if self._score1 == MAX_SCORE:
            return self._player1.get_intra_id(), self._player2.get_intra_id()
        elif self._score2 == MAX_SCORE:
            return self._player2.get_intra_id(), self._player1.get_intra_id()
        else:
            return None, None

    def set_player(self, player_intra_id: str, player_nickname: str) -> None:
        """
        플레이어를 설정하는 함수
        Args:
            player_intra_id: 플레이어의 intra_id
            player_nickname: 플레이어의 닉네임

        Returns:
            None
        """
        if self._player1 is None:
            self._player1 = Player(1, player_intra_id, player_nickname)
            return

        if self._player2 is None:
            self._player2 = Player(2, player_intra_id, player_nickname)
            return

    def set_ready(self, number: str) -> None:
        """
        플레이어의 상태를 준비로 설정하는 함수
        Args:
            number: 플레이어 번호

        Returns:
            None
        """
        if number == "player1":
            self._player1.set_status(PlayerStatus.READY)
        elif number == "player2":
            self._player2.set_status(PlayerStatus.READY)

    def set_status(self, status: GameStatus) -> None:
        """
        게임의 상태를 설정하는 함수
        Args:
            status: 게임의 상태

        Returns:
            None
        """
        self.__status = status
