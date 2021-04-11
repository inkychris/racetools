import enum


class GameState(enum.Enum):
    EXITED = 0
    FRONT_END = 1
    INGAME_PLAYING = 2
    INGAME_PAUSED = 3
    INGAME_INMENU_TIME_TICKING = 4
    INGAME_RESTARTING = 5
    INGAME_REPLAY = 6
    FRONT_END_REPLAY = 7


class SessionState(enum.Enum):
    INVALID = 0
    PRACTICE = 1
    TEST = 2
    QUALIFY = 3
    FORMATION_LAP = 4
    RACE = 5
    TIME_ATTACK = 6
