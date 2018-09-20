from context import context
from ui.screen.list_profiles import ListProfiles
from ui.screen.create_profile import CreateProfile
from ui.screen.create_goals import CreateGoal
from ui.screen.checkin import Checkin
from ui.screen.shop import Shop

class ScreenManager:
  def __init__(self):
    self.screen_map = {}
    self.screen_map['list_profiles'] = ListProfiles
    self.screen_map['create_profile'] = CreateProfile
    self.screen_map['create_goal'] = CreateGoal
    self.screen_map['checkin'] = Checkin
    self.screen_map['shop'] = Shop
    self.bread_crumbs = []
    self.screen = None
  def set_home(self):
    self.set_screen('list_profiles')
  def set_screen(self, name):
    self.screen = self.screen_map[name](self)
    self.bread_crumbs.append(name)
  def select_profile(self):
    profile = context['profile']
    if any(x.end_date == None for x in profile.goals):
      self.set_screen('checkin')
    else:
      self.set_screen('create_goal')
  def back(self):
    self.bread_crumbs.pop()
    name = self.bread_crumbs.pop()
    self.set_screen(name)
