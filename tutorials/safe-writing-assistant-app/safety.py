"""The checks that need no model call. They run first, so a bad request costs nothing."""

MAX_DRAFT_CHARS = 1500


class Rejected(Exception):
    """A request we refuse. The message is safe to show to the user."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def check_length(draft):
    draft = (draft or "").strip()
    if not draft:
        raise Rejected("Paste a draft first. The box is empty.")
    if len(draft) > MAX_DRAFT_CHARS:
        raise Rejected(f"The draft has {len(draft)} characters. The limit is {MAX_DRAFT_CHARS}.")
    return draft
