# File demonstrating the DictDataWidget and ListDataWidget classes.

from __future__ import annotations
from typing import (
    Any,
    Generic,
    TypeVar,
    Dict,
    Iterator,
    ItemsView,
    KeysView,
    ValuesView,
)

import rich.repr
from textual.widget import Widget
from textual.message import Message


T = TypeVar("T")


class ListDataWidget(Widget, Generic[T]):
    """ListDataWidget is a simple list-like widget for Textual.
    This is only used by the demo app, not by the FigletWidget.

    The reason this is in its own module is that its a very useful generic widget,
    and so I wanted to keep it seperate from the demo app for future reference.

    The reason this exists at all is because it can be queried using Textual's query system.
    This is a better way to store data on the main app class than simply doing something
    like `self.app.my_list_foo`. Type checkers do not like self.app.my_list_foo. (It is
    only determined at runtime). If you've ever tried to do this with your type
    checker in strict mode, you know what I mean.

    By making a ListDataWidget and mounting it to the app class (hidden), we can use the
    query system instead of self.app.my_list_foo. This provides much better type checking
    and it makes Pyright and MyPy happy without needing to use any '#type: ignore' comments.
    """

    class Updated(Message):

        def __init__(self, widget: ListDataWidget[T]) -> None:
            super().__init__()
            self.widget = widget
            "The ListDataWidget that was updated."

    list: list[T] = []

    def __init__(self):
        """Initialize the ListDataWidget.
        There are no arguments to pass in.
        TODO: This should take a list of items to start with to be more versatile."""

        super().__init__()
        self.display = False
        self.list = []

    def __rich_repr__(self) -> rich.repr.Result:
        yield "Items in ListDataWidget:"
        for item in self.list:
            try:
                yield str(item)
            except Exception:
                yield repr(item)

    def __getitem__(self, index: int) -> T:
        return self.list[index]

    def __setitem__(self, index: int, value: T) -> None:
        self.list[index] = value

    def __delitem__(self, index: int) -> None:
        del self.list[index]

    def __len__(self) -> int:
        return len(self.list)

    def __iter__(self) -> Iterator[T]:
        return iter(self.list)

    def append(self, item: T) -> None:
        self.list.append(item)
        self.post_message(self.Updated(self))

    def extend(self, other: list[T]) -> None:
        self.list.extend(other)
        self.post_message(self.Updated(self))

    def insert(self, index: int, item: T) -> None:
        self.list.insert(index, item)
        self.post_message(self.Updated(self))

    def remove_item(self, item: T) -> None:
        self.list.remove(item)
        self.post_message(self.Updated(self))

    def pop(self, index: int = -1) -> T:
        self.post_message(self.Updated(self))
        return self.list.pop(index)

    def clear(self) -> None:
        self.list.clear()
        self.post_message(self.Updated(self))

    def index(self, item: T, *args: Any) -> int:
        return self.list.index(item, *args)

    def count(self, item: T) -> int:
        return self.list.count(item)

    def copy(self) -> list[T]:
        return self.list.copy()


K = TypeVar("K")
V = TypeVar("V")


class DictDataWidget(Widget, Generic[K, V]):

    store: Dict[K, V] = {}

    def __init__(self):
        super().__init__()
        self.display = False  # <-- This keeps it hidden in the DOM
        self.store = {}  #      <-- Initialize a fresh dictionary for each instance

    def __getitem__(self, key: K) -> V:
        return self.store[key]

    def __setitem__(self, key: K, value: V) -> None:
        self.store[key] = value

    def __delitem__(self, key: K) -> None:
        del self.store[key]

    def __contains__(self, key: object) -> bool:
        return key in self.store

    def __len__(self) -> int:
        return len(self.store)

    def __iter__(self) -> Iterator[K]:
        return iter(self.store)

    def keys(self) -> KeysView[K]:
        return self.store.keys()

    def values(self) -> ValuesView[V]:
        return self.store.values()

    def items(self) -> ItemsView[K, V]:
        return self.store.items()

    def update(self, other_dict: Dict[K, V]) -> None:
        self.store.update(other_dict)

    def get(self, key: K, default: Any = None) -> V | Any:
        return self.store.get(key, default)
