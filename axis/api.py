"""API management class and base class for the different end points."""

import logging
from pprint import pformat
from typing import (
    Any,
    Callable,
    ItemsView,
    Iterator,
    KeysView,
    List,
    Optional,
    ValuesView,
)

import attr

LOGGER = logging.getLogger(__name__)

CONTEXT = "Axis library"


@attr.s
class Body:
    """Create API request body."""

    method: str = attr.ib()
    apiVersion: str = attr.ib()
    context: str = attr.ib(default=CONTEXT)
    params: Any = attr.ib(factory=dict)


class APIItem:
    """Base class for all end points using APIItems class."""

    def __init__(self, id: str, raw: dict, request: Callable) -> None:
        """Initialize API item."""
        self._id = id
        self._raw = raw
        self._request = request

        self.observers: List[Callable] = []

    @property
    def id(self) -> str:
        """Read only ID."""
        return self._id

    @property
    def raw(self) -> dict:
        """Read only raw data."""
        return self._raw

    def update(self, raw: dict) -> None:
        """Update raw data and signal new data is available."""
        self._raw = raw

        for observer in self.observers:
            observer()

    def register_callback(self, callback: Callable) -> None:
        """Register callback for state updates."""
        self.observers.append(callback)

    def remove_callback(self, observer: Callable) -> None:
        """Remove observer."""
        if observer in self.observers:
            self.observers.remove(observer)


class APIItems:
    """Base class for a map of API Items."""

    def __init__(self, raw, request, path, item_cls) -> None:
        """Initialize API items."""
        self._request = request
        self._path = path
        self._item_cls = item_cls
        self._items: dict = {}
        self.process_raw(raw)
        LOGGER.debug(pformat(raw))

    async def update(self) -> None:
        """Refresh data."""
        raw = await self._request("get", self._path)
        self.process_raw(raw)

    @staticmethod
    def pre_process_raw(raw: dict) -> dict:
        """Allow childs to pre-process raw data."""
        return raw

    def process_raw(self, raw: Any) -> set:
        """Process raw and return a set of new IDs."""
        new_items = set()

        for id, raw_item in self.pre_process_raw(raw).items():
            obj = self._items.get(id)

            if obj is not None:
                obj.update(raw_item)
            else:
                self._items[id] = self._item_cls(id, raw_item, self._request)
                new_items.add(id)

        return new_items

    def items(self) -> ItemsView[str, APIItem]:
        """Return items."""
        return self._items.items()

    def keys(self) -> KeysView[str]:
        """Return item keys."""
        return self._items.keys()

    def values(self) -> ValuesView[APIItem]:
        """Return item values."""
        return self._items.values()

    def get(self, obj_id: str, default: Optional[Any] = None):
        """Get item value based on key, return default if no match."""
        if obj_id in self:
            return self[obj_id]
        return default

    def __getitem__(self, obj_id: str) -> APIItem:
        """Get item value based on key."""
        return self._items[obj_id]

    def __iter__(self) -> Iterator[str]:
        """Allow iterate over items."""
        return iter(self._items)

    def __contains__(self, obj_id: str) -> bool:
        """Validate membership of item ID."""
        return obj_id in self._items

    def __len__(self) -> int:
        """Return number of items in class."""
        return len(self._items)

    def __bool__(self) -> bool:
        """Return True.

        Needs to define this because __len__ asserts false on length 0.
        """
        return True
