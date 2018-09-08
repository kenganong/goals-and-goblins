from context import context
from ui.component.text_entry import TextEntry

class CreateProfile:
  def __init__(self):
    font = context['ui_font']
    label_color = context['ui_label_text_color']
    bg_color = context['ui_background_color']
    self.label = font.render('Enter Profile Name', False, label_color)
    self.text_entry = TextEntry((100, 150), font, label_color, bg_color)
    self.text_entry.focus = True
    self.painted = False
    self.next_screen = None
  def paint(self, screen):
    screen.blit(self.label, (100, 50))
    self.painted = True
  def update(self, screen):
    self.text_entry.update(screen)
  def handle_event(self, event):
    self.text_entry.handle_event(event)
