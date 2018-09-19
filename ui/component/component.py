class Component:
  def __init__(self, position):
    self.position = position
    self.dirty = True
    self.focus = False
  def update(self, screen):
    if self.dirty:
      screen.blit(self.surface, self.position)
      self.dirty = False
