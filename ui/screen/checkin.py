from context import context
from ui.component.label import Label

class Checkin:
  def __init__(self, manager):
    self.manager = manager
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Checkin', theme.label_text_color, theme.background_color)
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.label.update(screen)
  def handle_event(self, event):
    pass
