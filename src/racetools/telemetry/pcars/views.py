import abc

import racetools.telemetry.pcars.enums as pcars_enums
import racetools.telemetry.pcars.udp as pcars_udp


class DataSet:
    def __init__(self, udp: pcars_udp.Data = None):
        self._udp = udp or pcars_udp.Data()

    @property
    def udp(self):
        return self._udp


class _DataView(abc.ABC):
    def __init__(self, data: DataSet):
        self._data = data
        self._get_udp = self._data.udp.get


class _IndexedDataView(_DataView, abc.ABC):
    def __init__(self, data: DataSet, index: int):
        super().__init__(data)
        self._index = index


class GameView(_DataView):
    """
    Query the state of the game.
    Note that "INGAME_PAUSED" and "EXITED" states
    do not appear to be sent by Project Cars 2 via UDP.
    """

    @property
    def state(self) -> pcars_enums.GameState:
        """
        Return the raw game state enum value.
        """
        raw = self._get_udp(pcars_udp.GameStateData, 'game_state')
        return pcars_enums.GameState(raw & 0b1111)

    @property
    def in_main_menu(self) -> bool:
        """
        Returns ``True`` if the game was in the main menu.
        """
        return self.state == pcars_enums.GameState.FRONT_END

    @property
    def is_playing(self) -> bool:
        """
        Returns ``True`` if the player is driving.
        """
        return self.state == pcars_enums.GameState.INGAME_PLAYING

    @property
    def in_session_menu(self) -> bool:
        """
        Returns ``True`` if the player is in a menu
        while the session time is still ticking.
        """
        return self.state == pcars_enums.GameState.INGAME_INMENU_TIME_TICKING

    @property
    def session_restarting(self) -> bool:
        """
        Returns ``True`` if the session is restarting.
        """
        return self.state == pcars_enums.GameState.INGAME_RESTARTING

    @property
    def in_session(self):
        """
        Returns ``True`` if the player is in a session.
        """
        min_in_game = pcars_enums.GameState.INGAME_PLAYING.value
        max_in_game = pcars_enums.GameState.INGAME_REPLAY.value
        return min_in_game <= self.state.value <= max_in_game

    @property
    def in_replay(self) -> bool:
        """
        Returns ``True`` if the player is viewing a replay,
        either in a session, or from the main menu.
        """
        return self.state in (pcars_enums.GameState.FRONT_END_REPLAY, pcars_enums.GameState.INGAME_REPLAY)
