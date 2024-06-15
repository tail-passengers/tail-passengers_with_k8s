from enum import Enum
from typing import Final

FIELD_WIDTH: Final = 1200
FIELD_LENGTH: Final = 3000
PADDLE_WIDTH: Final = 200
PADDLE_HEIGHT: Final = 30
PADDLE_SPEED: Final = 30
PADDLE_CORRECTION: Final = 10
BALL_SPEED_X: Final = 0
BALL_SPEED_Z: Final = 30
BALL_RADIUS: Final = 20
MAX_SCORE: Final = 3
PADDLE_BOUNDARY: Final = FIELD_WIDTH // 2 - PADDLE_WIDTH // 2
TOURNAMENT_PLAYER_MAX_CNT: Final = 4
NOT_ALLOWED_TOURNAMENT_NAME: Final = "wait"
MAX_TOURNAMENT_NAME_LENGTH: Final = 20


class KeyboardInput(Enum):
    """
    키보드 입력에 대한 Enum 클래스
    """

    LEFT_PRESS = "left_press"
    LEFT_RELEASE = "left_release"
    RIGHT_PRESS = "right_press"
    RIGHT_RELEASE = "right_release"
    SPACE = "space"


class PlayerStatus(Enum):
    """
    플레이어의 상태에 대한 Enum 클래스
    """

    WAIT = "wait"
    READY = "ready"
    ROUND_READY = "round_ready"
    PLAYING = "playing"
    SCORE = "score"
    END = "end"


class GameStatus(Enum):
    """
    게임의 상태에 대한 Enum 클래스
    """

    WAIT = "wait"
    READY = "ready"
    ROUND_READY = "round_ready"
    PLAYING = "playing"
    SCORE = "score"
    END = "end"
    ERROR = "error"


class MessageType(Enum):
    """
    메시지의 타입에 대한 Enum 클래스
    """

    WAIT = "wait"
    CREATE = "create"
    READY = "ready"
    START = "start"
    PLAYING = "playing"
    SCORE = "score"
    END = "end"
    COMPLETE = "complete"
    ERROR = "error"
    STAY = "stay"


class GameTimeType(Enum):
    """
    게임 시간에 대한 Enum 클래스
    """

    START_TIME = "start_time"
    END_TIME = "end_time"


class RoundNumber(Enum):
    """
    라운드 번호에 대한 Enum 클래스
    """

    ROUND_1 = "1"
    ROUND_2 = "2"
    ROUND_3 = "3"
    FINAL_NUMBER = "3"


class TournamentStatus(Enum):
    """
    토너먼트 상태에 대한 Enum 클래스
    """

    WAIT = "wait"
    READY = "ready"
    PLAYING = "playing"
    END = "end"
    ERROR = "error"


class ResultType(Enum):
    """
    결과에 대한 Enum 클래스
    """

    SUCCESS = "success"
    FAIL = "fail"


class PlayerNumber(Enum):
    """
    플레이어 번호에 대한 Enum 클래스
    """

    PLAYER_1 = "player1"
    PLAYER_2 = "player2"
    PLAYER_3 = "player3"
    PLAYER_4 = "player4"


class TournamentGroupName(Enum):
    """
    토너먼트 그룹 이름에 대한 Enum 클래스
    """

    A_TEAM = "a_team"
    B_TEAM = "b_team"
    FINAL_TEAM = "final_team"
