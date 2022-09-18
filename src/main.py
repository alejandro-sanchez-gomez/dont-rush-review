
#!/usr/bin/env python

"""
Provides everything necessary to make the addon work:
- Adds HTML and JavaScript content to Deck Configuration from the options folder.
- Prevents the revelation of the card's answer.
- Freezes the card answer a number of seconds so you can retain its content.
"""

# Speed Focus Mode Add-on for Anki
#
# Copyright (C) 2022  Alejandro Sánchez <https://github.com/Levantin00>
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
# listed here: <https://github.com/Levantin00>.
#
# Any modifications to this file must keep this entire header intact.

# -*- coding: utf-8 -*-

import os
from aqt import gui_hooks
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from anki.hooks import wrap
from anki.lang import _
import time
import json

#
# VARIABLES
#

currentPath = os.path.dirname(__file__)
optionsPath = os.path.join(currentPath, 'options')
htmlPath = os.path.join(optionsPath, 'options.html')
jsPath = os.path.join(optionsPath, 'options.js')

with open(htmlPath, encoding="utf8") as f:
    html = f.read()
with open(jsPath, encoding="utf8") as f:
    js = f.read()

#
# FUNCTIONS
#

def on_mount(dialog):
    dialog.web.eval(js.replace("HTML_CONTENT", json.dumps(html)))

def stop_ease(self, placeholder1, placeholder2):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    time.sleep(c['minTimeEase'])

def stop_answer(self, *, _old):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    if self.card.timeTaken() < (c['minTimeAnswer'] * 1000):
        return
    return _old(self)

#
# HOOKS
#

Reviewer._showAnswer = wrap(Reviewer._showAnswer, stop_answer, "around")
gui_hooks.deck_options_did_load.append(on_mount)
gui_hooks.reviewer_did_answer_card.append(stop_ease)
