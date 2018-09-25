import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

context = {}

def create_db_session(db_name):
  if not db_name.endswith('.db'):
    db_name += '.db'
  engine = create_engine('sqlite:///' + db_name)
  Base.metadata.bind = engine
  DBSession = sessionmaker(bind=engine)
  session = DBSession()
  context['db_session'] = session
  return session

def set_size(width, height):
  context['width'] = width
  context['height'] = height

def set_theme():
  theme = Theme()
  context['theme'] = theme
  theme.font = pygame.font.SysFont('timesnewroman', 24)
  theme.small_font = pygame.font.SysFont('timesnewroman', 12)
  black = pygame.Color('black')
  white = pygame.Color('white')
  grey = pygame.Color(50, 50, 50)
  green = pygame.Color(0, 150, 0)
  bright_green = pygame.Color(0, 200, 0)
  theme.background_color = black
  theme.label_text_color = white
  theme.entry_text_color = white
  theme.entry_background_color = grey
  theme.button_text_color = white
  theme.button_color = green
  theme.button_focus_color = bright_green
  theme.button_disabled_color = grey

class Theme:
  pass
