import abc

import racetools.util.types

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
    Note that "INGAME_PAUSED" does not appear
    to be sent by Project Cars 2 via UDP.
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


class SessionView(_DataView):
    """
    Query the state of the session.
    """

    @property
    def state(self) -> pcars_enums.SessionState:
        """
        Return the raw session state enum value.
        """
        raw = self._get_udp(pcars_udp.GameStateData, 'game_state')
        return pcars_enums.SessionState(raw >> 4)

    @property
    def is_practice(self) -> bool:
        """
        Returns ``True`` if player is in a practice session.
        """
        return self.state == pcars_enums.SessionState.PRACTICE

    @property
    def is_test(self):
        """
        Returns ``True`` if player is in a test session.
        This has not yet been reproduced in game
        so this property may be of limited use.
        """
        return self.state == pcars_enums.SessionState.TEST

    @property
    def is_qualifying(self):
        """
        Returns ``True`` if player is in a qualifying session.
        """
        return self.state == pcars_enums.SessionState.QUALIFY

    @property
    def is_formation_lap(self):
        """
        Returns ``True`` if player is on a formation lap.
        """
        return self.state == pcars_enums.SessionState.FORMATION_LAP

    @property
    def is_race(self):
        """
        Returns ``True`` if player is in a race session.
        Returns ``False`` when in a race but on a formation lap.
        """
        return self.state == pcars_enums.SessionState.RACE

    @property
    def is_time_trial(self):
        """
        Returns ``True`` if player is in a time-trial session.
        """
        return self.state == pcars_enums.SessionState.TIME_ATTACK


class ParticipantView(_IndexedDataView):
    """
    Retrieve properties on a participant in a session.
    """
    @property
    def _session_index1(self):
        return self._get_udp(pcars_udp.ParticipantsData, key='index', array_index=self._index)

    @property
    def _session_index2(self):
        return self._get_udp_timings_participants('participant_index')

    @property
    def name(self) -> str:
        raw = self._get_udp(pcars_udp.ParticipantsData, key='name', array_index=self._index)
        return racetools.util.types.c_string_to_str(raw)

    def _get_udp_timings_participants(self, key):
        return self._get_udp(
            pcars_udp.TimingsData,
            key='participants',
            array_index=self._index,
            array_key=key)

    @property
    def is_active(self) -> bool:
        return bool(self._get_udp_timings_participants('race_position') >> 7)

    @property
    def is_human(self) -> bool:
        return bool(self._get_udp_timings_participants('car_index') >> 15)

    @property
    def race_position(self) -> int:
        return self._get_udp_timings_participants('race_position') & 0b01111111

    @property
    def sector(self) -> int:
        return self._get_udp_timings_participants('sector') & 0b00000011
