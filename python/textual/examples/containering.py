from textual.containers import Vertical, Container, Horizontal, VerticalGroup
from textual.widgets import Static, Select, OptionList, RichLog
from textual.app import App, ComposeResult


class TestApp(App):
    DEFAULT_CSS = """
    RichLog {
        height: 80%;
        border: solid orange;
    }
    #stage_select {
        max-width: 80;
        border: solid orange;
    }
    #level_select {
        max-width: 30;
        border: solid orange;
    }
    #job_log {
        background: $panel;
        border: solid orange;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Horizontal() as h:
            h.styles.border = ("solid", "blue")
            with VerticalGroup() as v:
                v.styles.border = ("solid", "yellow")
                v.styles.max_width = 80
                yield Select(
                    [(v, k) for k, v in [("DEBUG", "DEBUG")]],
                    value="DEBUG",
                    id="level_select",
                    allow_blank=False,
                )
                stages = {"stage1": "Stage 1", "stage2": "Stage 2", "stage3": "Stage 3"}
                if stages:
                    ol = OptionList(*stages.values(), id="stage_select")
                    ol.styles.height = 10
                    yield ol
            l = RichLog(id="job_log")
            l.auto_scroll = True
            yield l


if __name__ == "__main__":
    app = TestApp()
    app.run()
