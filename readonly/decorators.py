from contextlib import contextmanager

from django.db.backends import utils

from readonly.cursor import (
    PatchedCursorWrapper,
    PatchedCursorDebugWrapper,
)

_orig_CursorWrapper = utils.CursorWrapper
_orig_CursorDebugWrapper = utils.CursorDebugWrapper


class ForcedPatchedCursorWrapper(PatchedCursorWrapper):
    def __init__(self, cursor, db):
        super(ForcedPatchedCursorWrapper, self).__init__(cursor, db, read_only=True)


class ForcedPatchedCursorDebugWrapper(PatchedCursorDebugWrapper):
    def __init__(self, cursor, db):
        super(ForcedPatchedCursorDebugWrapper, self).__init__(
            cursor, db, read_only=True
        )


@contextmanager
def readonly():
    old_CursorWrapper = utils.CursorWrapper
    old_CursorDebugWrapper = utils.CursorDebugWrapper
    utils.CursorWrapper = ForcedPatchedCursorWrapper
    utils.CursorDebugWrapper = ForcedPatchedCursorDebugWrapper
    try:
        yield
    finally:
        utils.CursorWrapper = old_CursorWrapper
        utils.CursorDebugWrapper = old_CursorDebugWrapper


@contextmanager
def write_enabled():
    old_CursorWrapper = utils.CursorWrapper
    old_CursorDebugWrapper = utils.CursorDebugWrapper
    utils.CursorWrapper = _orig_CursorWrapper
    utils.CursorDebugWrapper = _orig_CursorDebugWrapper
    try:
        yield
    finally:
        utils.CursorWrapper = old_CursorWrapper
        utils.CursorDebugWrapper = old_CursorDebugWrapper
