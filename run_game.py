import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Profile

def main():
  engine = create_engine('sqlite:///goalsgoblins.db')
  Base.metadata.bind = engine
  DBSession = sessionmaker(bind=engine)
  session = DBSession()

  profiles = session.query(Profile).order_by(Profile.name).all()

  pygame.init()

  width = 800
  height = 800
  screen = pygame.display.set_mode((width,height))
  clock = pygame.time.Clock()
  running = True

  font = pygame.font.SysFont('timesnewroman', 24)
  white = pygame.Color('white')
  green = pygame.Color(0, 150, 0)
  bright_green = pygame.Color(0, 200, 0)

  buttons = [Button(pygame.Rect(100, 150 + 100 * idx, 600, 98), font, profile.name, white, green, bright_green)
               for idx, profile in enumerate(profiles)]

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    mouse_pos = pygame.mouse.get_pos()

    label = font.render('Choose Profile', False, white)
    screen.blit(label, (100, 50))
    # A rect is (left, top, width, height)
    for button in buttons:
      button.register_mouse(mouse_pos)
      button.update(screen)
    pygame.display.flip()
    clock.tick(15)

class Button:
  def __init__(self, rect, font, text, text_color, button_color, focus_color):
    self.rect = rect
    self.label = font.render(text, False, text_color)
    self.label_rect = self.label.get_rect()
    self.label_rect.center = self.rect.center
    self.color = button_color
    self.focus_color = focus_color
    self.focus = False
    self.changed = True
  def register_mouse(self, mouse_pos):
    collide = self.rect.collidepoint(mouse_pos)
    if collide and not self.focus:
      self.focus = True
      self.changed = True
    elif not collide and self.focus:
      self.focus = False
      self.changed = True
  def update(self, surface):
    if self.changed:
      if self.focus:
        color = self.focus_color
      else:
        color = self.color
      pygame.draw.rect(surface, color, self.rect)
      surface.blit(self.label, self.label_rect)
      self.changed = False

# Run the main function only if this module is the main script
if __name__=="__main__":
  main()
