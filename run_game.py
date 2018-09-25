import pygame
import context
from model import Base, Profile
from ui.screen.screen_manager import ScreenManager
from ui.component.button import Button

def main():
  pygame.init()

  session = context.create_db_session('goalsgoblins')
  context.set_theme()
  profiles = session.query(Profile).order_by(Profile.name).all()

  context.set_size(1000, 800)
  surface = pygame.display.set_mode((context.context['width'], context.context['height']))
  clock = pygame.time.Clock()
  running = True

  sm = ScreenManager()
  sm.set_home()

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      else:
        sm.screen.handle_event(event)

    if not sm.screen.painted:
      surface.fill(context.context['theme'].background_color)
      sm.screen.paint(surface)
    else:
      sm.screen.update(surface)

    pygame.display.flip()
    clock.tick(15)

# Run the main function only if this module is the main script
if __name__=="__main__":
  main()
