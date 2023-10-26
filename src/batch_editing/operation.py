# -*- coding: utf-8 -*-

# Batch Editing Add-on for Anki
#
# Copyright (C) 2016-2023  Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.


from typing import TYPE_CHECKING, Callable, Optional, Sequence

from anki.collection import OpChangesWithCount
from aqt.operations import CollectionOp
from aqt.qt import QWidget
from .collection import edit_notes, EditMode

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import NoteId


def batch_edit_notes(
    parent: QWidget,
    mode: EditMode,
    note_ids: Sequence["NoteId"],
    field_name: str,
    html: str,
    is_html: bool,
    on_complete: Optional[Callable[[int], None]] = None,
):
    def on_success(changes: OpChangesWithCount):
        if not on_complete:
            return
        on_complete(changes.count)

    def operation(collection: "Collection") -> OpChangesWithCount:
        modified_notes = edit_notes(
            collection=collection,
            note_ids=note_ids,
            mode=mode,
            field_name=field_name,
            html=html,
            is_html=is_html,
        )

        undo_entry_id = collection.add_custom_undo_entry("Batch Edit")
        changes = collection.update_notes(modified_notes)
        collection.merge_undo_entries(undo_entry_id)

        return OpChangesWithCount(changes=changes, count=len(modified_notes))

    CollectionOp(parent=parent, op=operation).success(on_success).run_in_background()
