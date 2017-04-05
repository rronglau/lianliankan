# game_functions.py
# coding: utf-8
import pygame
import random
import sys
from copy import deepcopy

pygame.init()
screen_width, screen_height = 800, 600
num_pic = 25
bg_color = (230, 230, 230)
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill(bg_color)
row_num = 10
column_num = 10
pic_width = int(screen_width / column_num)
pic_height = int(screen_height / row_num)

last_pos = (-1, -1)

# @m: the number of rows;
# @n: the number of columns;
# @return: a list of points;
def get_point_list(m, n):
	point_list = []
	for x in range(m):
		for y in range(n):
			point = (x, y)
			point_list.append(point)
	return point_list
	
def check_events(image_dict):
	"""响应鼠标及按键事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			get_mouse_pos(event, image_dict)
		    
# @m: the number of rows;
# @n: the number of columns;
# @return: a dict mapping from pos(x, y) to image index.
def get_map(m, n):
	"""根据指定图片数量及图片像素生成连连看基础图片"""
	new_list = get_point_list(m, n)
	items = []
	# 每张图片重复出现4次
	for i in range(4):
		for j in range(num_pic):
			image = pygame.image.load("images/%d.jpg" %j)
			# 根据要求统一重置图片的像素
			image = pygame.transform.scale(image, (pic_width, pic_height))
			# 随机取出列表的一个元素
			pos = random.choice(new_list)
			# 创建包含选定列表坐标及图片编号的列表
			items.append((pos,j))
			# 根据图片遍历及所取出的随机像素点在屏幕上显示图片
			posPixel = (pos[0] * pic_width, pos[1] * pic_height)
			screen.blit(image, posPixel)
			pygame.display.update()
			# 将已显示图片的点从列表中删除
			new_list.remove(pos)
	return dict(items)
	
def get_mouse_pos(event, image_dict):
	"""响应按键"""
	global last_pos
	if pygame.mouse.get_pressed()[0]:
		# 单击鼠标左键，获取图片所在点坐标
		px, py = pygame.mouse.get_pos()
		cur_pos = pixel2pos(px, py)
		if cur_pos not in image_dict:
			return
		elif last_pos == (-1, -1):
			last_pos = cur_pos
			print("Get the first pos:", last_pos)
		elif cur_pos == last_pos:
			return
		else:
			# Now the first image is @last_pos;
			# the second image is (x, y).
			print("Get the second pos:", cur_pos,
				  "the first pos is", last_pos)
			if straight_connect(image_dict, cur_pos, last_pos) or\
				one_corner_connection(image_dict, cur_pos, last_pos) or\
				two_corners_connection(image_dict, cur_pos, last_pos):
				del_image_and_key(image_dict, cur_pos, last_pos)
				print("Well Done!")
			last_pos = (-1, -1)

# Given two points @pos1 and @pos2:
# 1. If they are not on the same line, return false;
# 2. Otherwise, if all the points between them (exclusive) are
# empty, return true;
# 3. Otherwise, return false;			
def is_empty_line(image_dict, pos1, pos2):
	print("is_empty_line:", pos1, pos2)
	if pos1[0] != pos2[0] and pos1[1] != pos2[1]:
		return False
	elif pos1[0] == pos2[0]:
		a = min(pos1[1], pos2[1])
		b = max(pos1[1], pos2[1])
		for i in range(a + 1, b):
			if (pos1[0], i)  in image_dict:
				return False
	elif pos1[1] == pos2[1]:
		a = min(pos1[0], pos2[0])
		b = max(pos1[0], pos2[0])
		for i in range(a + 1, b):
			if (i, pos1[1])  in image_dict:
				return False
					
	return True		
	
# Given two points @pos1 and @pos2:
def is_exclusive(image_dict, pos1, pos2):
	print("is_exclusive", pos1, pos2)
	pos3 = (pos1[0], pos2[1])
	pos4 =  (pos2[0], pos1[1])
	if is_empty_line(image_dict, pos1, pos3) and is_empty_line(image_dict, pos2, pos3)\
			and pos3 not in image_dict:	
		return True
	elif is_empty_line(image_dict, pos1, pos4) and is_empty_line(image_dict, pos2, pos4)\
			and pos4 not in image_dict:
		return True
	
			
# Given the current image pos and last image pos
# judge whether  they are the same picture	
# if same, then compare their x and y 
# judge whether they can connect or not	
def straight_connect(image_dict, pos1, pos2):
	pic1 = pos2pic(image_dict, pos1[0], pos1[1])
	pic2 = pos2pic(image_dict, pos2[0], pos2[1])
	print("stright_connect:", pos1, pos2, pic1, pic2)
	if pic1 == -1 or pic2 == -1:
		return False
	if pic1 == pic2:
		if (pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) == 1) or\
			(pos1[1] == pos2[1] and abs(pos1[0] - pos2[0]) == 1):			
			return True
		elif is_empty_line(image_dict, pos1, pos2):			
			return True
	return False
	
			
# Given the current image pos and last image pos
# judge whether  they are the same picture	
# if same, then suppose there is another point
# whose x is equal to image_1 and y is euqal to image2
def one_corner_connection(image_dict, pos1, pos2):
	pic1 = pos2pic(image_dict, pos1[0], pos1[1])
	pic2 = pos2pic(image_dict, pos2[0], pos2[1])
	print("one_corner_connection:", pos1, pos2, pic1, pic2)
	if pic1 == -1 or pic2 == -1:
		return False

	if pic1 == pic2:			
		if is_exclusive(image_dict, pos1, pos2):
			return True
	return False	

def two_corners_connection(image_dict, pos1, pos2):
	global row_num
	global column_num
	pic1 = pos2pic(image_dict, pos1[0], pos1[1])
	pic2 = pos2pic(image_dict, pos2[0], pos2[1])
	print("two_corners_connection", pos1, pos2, pic1, pic2)
	if pic1 == -1 or pic2 == -1:
		return False
	if pic1 == pic2:
		# Portrait scanning to search one point which
		# straight connect with pos1 and one_coener connection
		# with pos2
		for i in range(0, row_num):
			pos3 = (i, pos1[1])
			print("two_corners_connection", i, pos3)
			if is_empty_line(image_dict, pos1, pos3) and\
				is_exclusive(image_dict, pos2, pos3):
				print("Two corners connecting")
				return True
		# Transverse scanning to search one point which
		# straight connect with pos1 and one_coener connection
		# with pos2
		for j in range(0, column_num):
			pos3 = (pos1[0], j)
			print("two_corners_connection_second", j, pos3)
			if is_empty_line(image_dict, pos1, pos3) and\
				is_exclusive(image_dict, pos2, pos3):
				return True
	return False
			

# pos1 of pic1 , pos2 of pic2
# delete the images of two pos and the corresponding key
def del_image_and_key(image_dict, pos1, pos2):
	image_wipe(pos1[0], pos1[1])
	image_wipe(pos2[0], pos2[1])
	del image_dict[pos1]
	del image_dict[pos2]

					
def image_wipe(x, y):
	pixel = pos2pixel(x, y)
	rect_list=[pixel[0], pixel[1], pic_width, pic_height]
	pygame.draw.rect(screen, bg_color, rect_list, 0)		
	pygame.display.flip()		
			
				
# Given a pixel point(px, py), return the index of image by
# looking up the pos_to_image_index_dict dict.
# Return -1 if no image at (px, py).
def pixel2pic(image_dict, px, py):
	key = pixel2pos(px, py)
	return pos2pic(image_dict, key[0], key[1])
	
# Given a pos point(x, y), return the index of image by
# looking up the pos_to_image_index_dict dict.
# If there is no image at (x, y), return -1.
def pos2pic(image_dict, x, y):
	if (x, y) not in image_dict:
		return -1
	else:
		return image_dict[(x, y)]
	
def pos2pixel(x, y):	
	px = x * pic_width 
	py = y * pic_height
	return (px, py)
	
	
def pixel2pos(px, py):
	return (px // pic_width, py // pic_height)
	
def run_game():
	pos_to_image_index_dict = get_map(row_num, column_num)
	print(len(pos_to_image_index_dict))
	while True:
		check_events(pos_to_image_index_dict)
		
run_game()

		

