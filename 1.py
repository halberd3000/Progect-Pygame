import os
import sys
import pygame
import random
pygame.mixer.init()
pygame.mixer.music.load("Начало.wav")
pygame.mixer.music.play()
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
         pygame.mixer.music.stop()