# This was all done to add indexing abilities
# into the ListView class. Will probably turn this into a PR
# for Textual.
from __future__ import annotations
from typing import cast

from textual.message import Message
from textual.widgets import ListView, ListItem


class NewListView(ListView):

    #! Update this class:
    class Selected(Message):

        ALLOW_SELECTOR_MATCH = {"item"}

        def __init__(self, list_view: NewListView, item: ListItem, index: int) -> None:
            super().__init__()
            self.list_view: NewListView = list_view
            """The view that contains the item selected."""
            self.item: ListItem = item
            """The selected item."""
            self.index: int = index  # * <-- This line was added

        @property
        def control(self) -> NewListView:
            return self.list_view

    #! Update this method:
    def action_select_cursor(self) -> None:
        selected_child = self.highlighted_child
        if selected_child is None:
            return
        index = self._nodes.index(selected_child)
        self.post_message(
            self.Selected(self, selected_child, index)
        )  # * <-- This was modified (index)

    #! Update this method:
    def _on_list_item__child_clicked(self, event: ListItem._ChildClicked) -> None:  # type: ignore
        event.stop()
        self.focus()
        self.index = self._nodes.index(event.item)
        self.post_message(
            self.Selected(self, event.item, self.index)
        )  # * <-- This was modified (index)

    # * This was added:
    def __getitem__(self, index: int) -> ListItem:
        return cast(ListItem, self._nodes[index])
