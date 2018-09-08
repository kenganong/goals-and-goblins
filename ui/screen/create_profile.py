import pygame
from context import context
from ui.component.button import Button
from ui.component.text_entry import TextEntry

class CreateProfile:
  def __init__(self, manager):
    self.manager = manager
    font = context['ui_font']
    label_color = context['ui_label_text_color']
    bg_color = context['ui_background_color']
    text_color = context['ui_button_text_color']
    button_color = context['ui_button_color']
    focus_color = context['ui_button_focus_color']
    self.label = font.render('Name:', False, label_color)
    self.text_entry = TextEntry((110 + self.label.get_width(), 50), font, label_color, bg_color)
    self.text_entry.focus = True
    self.add_button = Button(self.create, pygame.Rect(100, 150, 600, 98),
                             font, 'Add', text_color, button_color, focus_color)
    self.cancel_button = Button(self.cancel, pygame.Rect(100, 250, 600, 98),
                                font, 'Cancel', text_color, button_color, focus_color)
    self.painted = False
  def paint(self, screen):
    screen.blit(self.label, (100, 50))
    self.update(screen)
    self.painted = True
  def update(self, screen):
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
      print('Creating {}'.format(name))
  def cancel(self):
    self.manager.set_screen('list_profiles')
