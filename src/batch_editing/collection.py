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

from typing import TYPE_CHECKING, Literal, Sequence

if TYPE_CHECKING:
    from aqt.browser.browser import Browser
    from anki.notes import NoteId


def batch_edit_notes(
    browser: "Browser",
    mode: Literal["adda", "addb", "replace"],
    nids: Sequence["NoteId"],
    fld: str,
    html: str,
    is_html: bool = False,
):
    if not is_html:
        # convert newlines to <br> elms
        html = html.replace("\n", "<br/>")
    mw = browser.mw
    mw.checkpoint("batch edit")
    mw.progress.start()
    browser.model.beginReset()
    cnt = 0
    for nid in nids:
        note = mw.col.get_note(nid)
        if fld in note:
            content = note[fld]
            if is_html:
                spacer = "\n"
                breaks = spacer
            else:
                breaks = ("<div>", "</div>", "<br>", "<br/>")
                spacer = "<br/>"
            if mode == "adda":
                if content.endswith(breaks):
                    spacer = ""
                note[fld] += spacer + html
            elif mode == "addb":
                if content.startswith(breaks):
                    spacer = ""
                note[fld] = html + spacer + content
            elif mode == "replace":
                note[fld] = html
            cnt += 1
            note.flush()
    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()
    return cnt
