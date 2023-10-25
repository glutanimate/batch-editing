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

"""
Initializes add-on components.
"""

from typing import TYPE_CHECKING, cast

from aqt.gui_hooks import browser_menus_did_init
from aqt.qt import QKeySequence, QMenu, QAction
from aqt.utils import tooltip

from .dialog import BatchEditDialog
from .gui import initialize_qt_resources

if TYPE_CHECKING:
    from aqt.browser.browser import Browser


def on_batch_edit(browser: "Browser"):
    if not (nids := browser.selectedNotes()):
        tooltip("No cards selected.")
        return
    if (collection := browser.mw.col) is None:
        return
    dialog = BatchEditDialog(browser=browser, collection=collection, nids=nids)
    dialog.exec()


def setup_menu(browser: "Browser"):
    menu: QMenu = browser.form.menuEdit
    menu.addSeparator()
    action = cast(QAction, menu.addAction("Batch Edit..."))
    action.setShortcut(QKeySequence("Ctrl+Alt+B"))
    action.triggered.connect(lambda _, b=browser: on_batch_edit(b))


initialize_qt_resources()
browser_menus_did_init.append(setup_menu)
