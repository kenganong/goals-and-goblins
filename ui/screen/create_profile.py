from datetime import date
import pygame
from context import context
from model import Profile
from ui.component.button import Button
from ui.component.label import Label
from ui.component.text_entry import TextEntry, ALPHA

class CreateProfile:
  def __init__(self, manager):
    self.manager = manager
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Name:', theme.label_text_color, theme.background_color)
    self.text_entry = TextEntry((110 + self.label.surface.get_width(), 50), 200, theme.font,
                                color=theme.entry_text_color, background=theme.entry_background_color)
    self.text_entry.set_allowed(ALPHA)
    self.text_entry.focus = True
    self.add_button = Button((100, 150), (600, 98), theme.font, 'Add', click_func=self.create,
                             text_color=theme.label_text_color, color=theme.button_color,
                             focus_color=theme.button_focus_color, disabled_color=theme.button_disabled_color)
    self.add_button.set_enabled(False)
    self.cancel_button = Button((100, 250), (600, 98), theme.font, 'Cancel', click_func=self.cancel,
                                text_color=theme.label_text_color, color=theme.button_color,
                                focus_color=theme.button_focus_color)
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.label.update(screen)
    self.text_entry.update(screen)
    self.add_button.update(screen)
    self.cancel_button.update(screen)
  def handle_event(self, event):
    self.text_entry.handle_event(event)
    self.add_button.set_enabled(len(self.text_entry.text) > 0)
    self.add_button.handle_event(event)
    self.cancel_button.handle_event(event)
  def create(self):
    name = self.text_entry.text
    if len(name) > 0:
      today = date.today().isoformat()
      profile = Profile(name=name, created_date=today, modified_date=today)
      session = context['db_session']
      session.add(profile)
      session.commit()
      self.manager.set_screen('list_profiles')
  def cancel(self):
    self.manager.set_screen('list_profiles')
