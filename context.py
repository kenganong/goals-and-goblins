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

def set_theme():
  font = pygame.font.SysFont('timesnewroman', 24)
  context['ui_font'] = font
  black = pygame.Color('black')
  white = pygame.Color('white')
  green = pygame.Color(0, 150, 0)
  bright_green = pygame.Color(0, 200, 0)
  context['ui_background_color'] = black
  context['ui_label_text_color'] = white
  context['ui_button_text_color'] = white
  context['ui_button_color'] = green
  context['ui_button_focus_color'] = bright_green
