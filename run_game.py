import pygame

def main():
  pygame.init()

  width = 800
  height = 400
  screen = pygame.display.set_mode((width,height))
  clock = pygame.time.Clock()
  running = True

  font = pygame.font.SysFont('timesnewroman', 24)
  white = pygame.Color('white')
  green = pygame.Color(0, 150, 0)
  bright_green = pygame.Color(0, 200, 0)

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    mouse_pos = pygame.mouse.get_pos()

    label = font.render('Choose Profile', False, white)
    screen.blit(label, (100, 50))
    # A rect is (left, top, width, height)
    rect = pygame.Rect(100, 150, 600, 98)
    rect_color = green
    if rect.collidepoint(mouse_pos):
      rect_color = bright_green
    pygame.draw.rect(screen, rect_color, rect)

    pygame.display.flip()
    clock.tick(15)

# Run the main function only if this module is the main script
if __name__=="__main__":
  main()
