from aqt import gui_hooks
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from aqt.utils import tr
from functools import partial

def remove_hard_and_easy_buttons(buttons, reviewer, card):
	new_buttons = []
	for ease, label in buttons:
		if ease == 1 or ease == reviewer._defaultEase():
			new_buttons.append((ease, label))
	return tuple(new_buttons)

def remap_hard_and_easy_to_good(ease_tuple, reviewer, card):
	cont, ease = ease_tuple
	if ease == 1:
		return ease_tuple
	else:
		return (cont, reviewer._defaultEase())

def get_second_answer_shortcut(reviewer) -> str:
	for key, cb in reviewer._shortcutKeys():
		if isinstance(cb, partial) and cb.func == reviewer._answerCard and cb.args == (2,):
			return key
	return "2"

def update_good_button_tooltip(self):
	tooltip = tr.actions_shortcut_key(val=get_second_answer_shortcut(self))
	self.bottom.web.eval(f'document.getElementById("defease").title = "{tooltip}";')

gui_hooks.reviewer_will_init_answer_buttons.append(remove_hard_and_easy_buttons)
gui_hooks.reviewer_will_answer_card.append(remap_hard_and_easy_to_good)
Reviewer._showEaseButtons = wrap(Reviewer._showEaseButtons, update_good_button_tooltip, 'after')
