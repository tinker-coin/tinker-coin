from datetime import datetime, timedelta, timezone

from constants.tinkerconstants import TINKER_EPOCH_MOMENT


class TinkerTimestamp:

    def __init__(self):
        self._ordinal: int = 0

    def __str__(self) -> str:
        return str(self._ordinal)

    def __repr__(self):
        return str(self.to_datetime())

    def to_ordinal(self) -> int:
        return self._ordinal

    def to_datetime(self) -> datetime:
        return TINKER_EPOCH_MOMENT + timedelta(seconds=self._ordinal)

    def to_str(self):
        return self._ordinal

    @staticmethod
    def from_ordinal(ordinal: int):
        t = TinkerTimestamp()
        t._ordinal = ordinal
        return t

    @staticmethod
    def from_datetime(_datetime: datetime):
        t = TinkerTimestamp()
        t._ordinal = int((_datetime - TINKER_EPOCH_MOMENT).total_seconds())
        return t

    @staticmethod
    def now():
        return TinkerTimestamp.from_datetime(datetime.now(tz=timezone.utc))
