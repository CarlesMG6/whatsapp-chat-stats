from biggest_sender import biggest_sender
from characters_per_day import characters_per_day
from days_without_messages import days_without_messages
from messages_per_day import messages_per_day
from streak_image_generator import streak_image_generator
from streaks_without_messages import streaks_without_messages
from mean_characters_per_message import mean_characters_per_message
from word_counter import word_counter
import os

name = 'Maincra'
directorio = name+ '/img'

if not os.path.exists(directorio):
    os.makedirs(directorio)

biggest_sender(name, directorio)
characters_per_day(name, directorio)
days_without_messages(name, directorio)
messages_per_day(name, directorio)
streak_image_generator(name, directorio)
streaks_without_messages(name, directorio)
mean_characters_per_message(name, directorio)
word_counter(name, directorio)


