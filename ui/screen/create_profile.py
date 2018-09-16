from datetime import date
import pygame
from context import context
from model import Profile
from ui.component.button import Button
from ui.component.label import Label
from ui.component.text_entry import TextEntry

class CreateProfile:
  def __init__(self, manager):
    self.manager = manager
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Name:', theme.label_text_color, theme.background_color)
    self.text_entry = TextEntry((110 + self.label.surface.get_width(), 50), 200, theme.font,
                                color=theme.label_text_color, background=theme.background_color)
    self.text_entry.focus = True
    self.add_button = Button(self.create, pygame.Rect(100, 150, 600, 98),
                             theme.font, 'Add', theme.button_text_color,
                             theme.button_color, theme.button_focus_color)
    self.cancel_button = Button(self.cancel, pygame.Rect(100, 250, 600, 98),
                                theme.font, 'Cancel', theme.button_text_color,
                                theme.button_color, theme.button_focus_color)
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
