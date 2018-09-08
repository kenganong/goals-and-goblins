from ui.screen.list_profiles import ListProfiles
from ui.screen.create_profile import CreateProfile

class ScreenManager:
  def __init__(self):
    self.screen_map = {}
    self.screen_map['list_profiles'] = ListProfiles
    self.screen_map['create_profile'] = CreateProfile
    self.bread_crumbs = []
    self.screen = None
  def set_home(self):
    self.set_screen('list_profiles')
  def set_screen(self, name):
    self.screen = self.screen_map[name](self)
    self.bread_crumbs.append(name)
  def back(self):
    self.bread_crumbs.pop()
    name = self.bread_crumbs.pop()
    self.set_screen(name)
