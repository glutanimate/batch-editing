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

from typing import TYPE_CHECKING, Sequence, cast

import os
import tempfile

from anki.lang import _
from aqt.qt import (
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QIcon,
    QKeySequence,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QShortcut,
    Qt,
    QVBoxLayout,
)
from aqt.utils import askUser, getFile, tooltip

from .collection import batch_edit_notes

if TYPE_CHECKING:
    from aqt.browser.browser import Browser
    from anki.notes import NoteId
    from anki.collection import Collection



class BatchEditDialog(QDialog):
    """Browser batch editing dialog"""

    def __init__(
        self, browser: "Browser", collection: "Collection", nids: Sequence["NoteId"]
    ):
        QDialog.__init__(self, parent=browser)
        self._browser = browser
        self._collection = collection
        self._nids = nids
        self.setup_ui()

    def setup_ui(self):
        text_field_label = QLabel("Content to add to or replace with:")
        image_button = QPushButton(self)
        image_button.clicked.connect(self.insert_media)
        image_button.setIcon(QIcon(":/batch-editing/icons/attach.svg"))
        image_button.setToolTip("Insert a media file reference (e.g. to an image)")
        press_action = QAction(self)
        press_action.triggered.connect(image_button.animateClick)
        press_action.setShortcut(QKeySequence(_("Alt+i")))
        image_button.addAction(press_action)
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(text_field_label)
        top_hbox.insertStretch(1, stretch=1)
        top_hbox.addWidget(image_button)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setTabChangesFocus(True)

        field_label = QLabel("In this field:")
        self.field_selector = QComboBox()
        fields = self.get_fields()
        self.field_selector.addItems(fields)
        f_hbox = QHBoxLayout()
        f_hbox.addWidget(field_label)
        f_hbox.addWidget(self.field_selector)
        f_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        button_box = QDialogButtonBox(Qt.Orientation.Horizontal, self)
        add_after_button = cast(
            QPushButton,
            button_box.addButton("Add &after", QDialogButtonBox.ButtonRole.ActionRole),
        )
        add_before_button = cast(
            QPushButton,
            button_box.addButton("Add &before", QDialogButtonBox.ButtonRole.ActionRole),
        )
        replace_button = cast(
            QPushButton,
            button_box.addButton("&Replace", QDialogButtonBox.ButtonRole.ActionRole),
        )
        close_button = cast(
            QPushButton,
            button_box.addButton("&Cancel", QDialogButtonBox.ButtonRole.RejectRole),
        )
        add_after_button.setToolTip("Add after existing field contents")
        add_before_button.setToolTip("Add before existing field contents")
        replace_button.setToolTip("Replace existing field contents")
        add_after_button.clicked.connect(lambda state, x="adda": self.on_confirm(x))
        add_before_button.clicked.connect(lambda state, x="addb": self.on_confirm(x))
        replace_button.clicked.connect(lambda state, x="replace": self.on_confirm(x))
        close_button.clicked.connect(self.close)

        self.checkbox_html = QCheckBox(self)
        self.checkbox_html.setText("Insert as HTML")
        self.checkbox_html.setChecked(False)
        shortcut = QShortcut(
            QKeySequence(_("Alt+H")),
            self,
        )
        shortcut.activated.connect(self.checkbox_html.toggle)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.addWidget(self.checkbox_html)
        bottom_hbox.addWidget(button_box)

        vbox_main = QVBoxLayout()
        vbox_main.addLayout(top_hbox)
        vbox_main.addWidget(self.text_edit)
        vbox_main.addLayout(f_hbox)
        vbox_main.addLayout(bottom_hbox)
        self.setLayout(vbox_main)
        self.text_edit.setFocus()
        self.setMinimumWidth(540)
        self.setMinimumHeight(400)
        self.setWindowTitle("Batch Edit Selected Notes")

    def get_fields(self):
        nid = self._nids[0]
        mw = self._browser.mw
        model = self._collection.getNote(nid).note_type()
        fields = self._collection.models.fieldNames(model)
        return fields

    def insert_media(self):
        media_file = self.get_clipboard()
        if not media_file:
            media_file = self.choose_file()
        if not media_file:
            return
        html = self._browser.editor._addMedia(media_file, canDelete=True)
        # need to unescape images again:
        html = self._collection.media.escapeImages(html, unescape=True)
        current = self.text_edit.toPlainText()
        new = []
        if current:
            # avoid duplicate newlines
            new = [*current.strip("\n").split("\n"), html]
            new = "\n".join(new)
        else:
            new = html
        self.text_edit.setPlainText(new)

    def choose_file(self):
        key = (
            _("Media")
            + " (*.jpg *.png *.gif *.tiff *.svg *.tif *.jpeg "
            + "*.mp3 *.ogg *.wav *.avi *.ogv *.mpg *.mpeg *.mov *.mp4 "
            + "*.mkv *.ogx *.ogv *.oga *.flv *.swf *.flac)"
        )
        return getFile(self, _("Add Media"), None, key, key="media")

    def get_clipboard(self):
        clip = QApplication.clipboard()
        if not clip or not clip.mimeData().imageData():
            return False
        handle, image_path = tempfile.mkstemp(suffix=".png")
        clip.image().save(image_path)
        clip.clear()
        if os.stat(image_path).st_size == 0:
            return False
        return image_path

    def on_confirm(self, mode):
        browser = self._browser
        nids = self._nids
        fld = self.field_selector.currentText()
        text = self.text_edit.toPlainText()
        isHtml = self.checkbox_html.isChecked()
        if mode == "replace":
            q = (
                "This will replace the contents of the <b>'{0}'</b> field "
                "in <b>{1} selected note(s)</b>. Proceed?"
            ).format(fld, len(nids))
            if not askUser(q, parent=self):
                return
        cnt = batch_edit_notes(browser, mode, nids, fld, text, isHtml=isHtml)
        self.close()
        tooltip("<b>Updated</b> {0} notes.".format(cnt), parent=browser)
