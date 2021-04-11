import abc

import racetools.telemetry.pcars.udp as pcars_udp


class DataSet:
    def __init__(self, udp: pcars_udp.Data):
        self._udp = udp

    @property
    def udp(self):
        return self._udp


class _DataView(abc.ABC):
    def __init__(self, data: DataSet):
        self._data = data


class _IndexedDataView(_DataView, abc.ABC):
    def __init__(self, data: DataSet, index: int):
        super().__init__(data)
        self._index = index
