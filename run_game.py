import pygame
import context
from model import Base, Profile
from ui.component.button import Button
from ui.screen.list_profiles import ListProfiles

def main():
  pygame.init()

  session = context.create_db_session('goalsgoblins')
  context.set_theme()
  profiles = session.query(Profile).order_by(Profile.name).all()

  width = 800
  height = 800
  surface = pygame.display.set_mode((width,height))
  clock = pygame.time.Clock()
  running = True

  screen = ListProfiles()

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    mouse_pos = pygame.mouse.get_pos()

    if not screen.painted:
      surface.fill(context.context['ui_background_color'])
      screen.paint(surface, mouse_pos)
    else:
      screen.update(surface, mouse_pos)

    pygame.display.flip()
    clock.tick(15)

# Run the main function only if this module is the main script
if __name__=="__main__":
  main()
