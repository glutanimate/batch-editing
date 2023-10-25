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

from enum import Enum
from typing import TYPE_CHECKING, Sequence, Union

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId


class EditMode(Enum):
    ADD_AFTER = 0
    ADD_BEFORE = 1
    REPLACE = 2


def edit_notes(
    collection: "Collection",
    note_ids: Sequence["NoteId"],
    mode: EditMode,
    field_name: str,
    html: str,
    is_html: bool,
) -> Sequence["Note"]:
    if not is_html:
        # convert newlines to <br> elms
        html = html.replace("\n", "<br/>")

    modified_notes: list["Note"] = []
    for nid in note_ids:
        note = collection.get_note(nid)
        if field_name in note:
            content = note[field_name]
            breaks: Union[str, tuple[str, ...]]

            if is_html:
                spacer = "\n"
                breaks = spacer
            else:
                breaks = ("<div>", "</div>", "<br>", "<br/>")
                spacer = "<br/>"

            if mode == EditMode.ADD_AFTER:
                if content.endswith(breaks):
                    spacer = ""
                note[field_name] += spacer + html
            elif mode == EditMode.ADD_BEFORE:
                if content.startswith(breaks):
                    spacer = ""
                note[field_name] = html + spacer + content
            elif mode == EditMode.REPLACE:
                note[field_name] = html
            else:
                print(f"Unsupported edit mode {mode}")
                continue

            modified_notes.append(note)
    return modified_notes
