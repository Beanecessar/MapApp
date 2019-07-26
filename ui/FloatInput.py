from kivy.uix.textinput import TextInput
import re

class FloatInput(TextInput):
	def __init__(self, *args, **kwargs):
		kwargs["multiline"] = False
		super().__init__(*args, **kwargs)

	ptn = re.compile('[^0-9]')
	def insert_text(self, substring, from_undo=False):
		if '.' in self.text:
		    s = re.sub(self.ptn, '', substring)
		else:
		    s = '.'.join([re.sub(self.ptn, '', s) for s in substring.split('.', 1)])
		return super(FloatInput, self).insert_text(s, from_undo=from_undo)