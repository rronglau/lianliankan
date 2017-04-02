# game_functions.py
# coding: utf-8
import pygame
import random
import sys
pygame.init()
screen_width, screen_height = 800, 600
pic_width = 80
pic_height = 60
num_pic = 25
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill((230, 230, 230))
m = 10
n = 10



def get_point_list(m, n):
	point_list = []
	for x in range(m):
		for y in range(n):
			point = (x, y)
			pixel_point = (screen_width / m * x,  screen_height / n * y)
			point_list.append(pixel_point)
	return point_list
	
	
def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				sys.exit()	
		    
def get_map(m, n, num_pic, pic_width, pic_height):
	new_list = get_point_list(m, n)
	for i in range(4):
		for j in range(num_pic):
			image = pygame.image.load("images/%d.jpg" %j)
			image = pygame.transform.scale(image, (pic_width, pic_height))
			setloc = random.choice(new_list)
			screen.blit(image, setloc)
			pygame.display.update()
			new_list.remove(setloc)
			
# def event_check:			
			

			
			
def run_game():
	get_map(m, n, num_pic, pic_width, pic_height)		
	while True:
		check_events()	
		
run_game()

		

